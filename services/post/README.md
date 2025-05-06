![tests](https://github.com/recourcefulcoder/VKCloneBackend/actions/workflows/post-tests.yml/badge.svg)

# POST service of VKCloneBackend


Table of contents:
---

- [Launching application](#running-an-application)
  - [In dev mode](#running-application-manually-so-called-in-dev-mode) (manually)
  - [With Docker Compose]()
- [Notes on testing](#testing-notes) (**MUST READ** before launching)
- [Documentation](#documentation)
  - [Endpoint docs](#endpoints-outline)
  - [File storage docs](#file-storage-documentation)
  - [Database](#database-documentation)
    - [Database migrations](#database-migrations)
  - [settings.py module](#settingspy-module)
  - [Environment variables](#environment-variables) 
  
## Running an application

This section contains instructions on how to run POST service - both manually and inside 
docker compose (yet isolated from other services for now)

### Running application manually (so-called "in dev mode")
1. Install dependencies

From root directory of the "user" service execute in your system's CLI and switch to "/src" directory:
```bash
pip install -r requirements.txt
cd src
```

2. Create .env file

Post service (just as any service, actually) requires some environment variables for 
its valid work. You can see full list of them [here](#environment-variables)
Specify this variables in .env file in the root directory of the service in following syntax:

    VARNAME1=value1
    VARNAME2=value2

> [!IMPORTANT]
> Set "POST_DEBUG" environment variable to _True_!

3. Create file storage directory, corresponding to [POST_DEBUG_FILE_STORAGE](#environment-variables) 
environment variable

4. Update PYTHONPATH with root directory of the service

To do that in Linux, run
```bash
export PYTHONPATH="path/to/root/dir/services/<service_name>:$PYTHONPATH"
```
5. Create PostgreSQL database and migrate with alembic

Create a PostgreSQL service, provide valid credentials for it in .env file (see above)
and migrate it using alembic. From the root directory of service, run:

```bash
alembic upgrade main@head
alembic upgrade dangerous@head
```

You may as well install some test data if you wish to test an application manually - 
it is done by using alembic's [branch "dev"](#database-migrations)
```bash
alembic upgrade dev@head
```

6. Run FastAPI

From "src" directory of the service run
```bash
fastapi dev main.py
``` 

6. _Enjoy ^\_^_


### Running with Docker Compose
              Not implemented yet

## Testing notes
Tests are not using mocking for database connections - meaning that they will violate data in the 
database they are operating upon. Since that it was decided that tests must run on a specially 
configured test database.

What is more - tests will not be run when environment variable POST_TESTING is not set to true - 
so make sure to configure your .env file properly before running tests

Tests have their own documentation, which is stored in ```tests/README.md```

### Instructions on setting up test environment 
1. Set up required [environment variables](#environment-variables)

Adjust .env file to include POST_TESTING=True and TEST_POSTGRES_DB=<name of your testing database> 
> POST_TESTING=True
> 
> TEST_POSTGRES_DB=post-service-test

2. Run migrations on test database

For that, from the root directory of the project execute:
```bash
alembic upgrade main@head
alembic upgrade dangerous@head
```
---
That's it - only thing left is to actually launch tests. You can do that by executing from the root (or /tests)
directory of the project:
```bash
pytest 
```

## Documentation

### Endpoints outline
This section defines complete list of requirements for the service endpoints, both
with information about which are implemented on the moment.

> [!NOTE]
> All actual interaction with files (meaning processing them and getting from server)
> are handled by Media Processing service (see main README.md in the root of the project),
> so until this service is implemented, post will actually not implement any logic related 
> to file I/O.

Endpoints table

> [!NOTE]
> _get_files_ endpoint which was defined in this document was moved to the 
> Media Processing service, as it contains logic related to file I/O. 

1. get_post 
- URL: /post/get/{post_id}/
- method: GET
- description: <br><br>
Returns information about single post with ID post_id; <br>
REQUEST doesn't have to contain any additional info <br> 
RESPONSE: on _invalid_ returns 404 on invalid ID value; on _valid_ ID returns JSON, containing post info in given format:
```json lines
{
  id: <post-id>,
  title: <post-title>,
  author_id: <id-of-posts-author>,
  
  content: <post-content>,
  
  creation_date: <creation-date>,  // in YYYY-MM-DDTHH:MM:SS.f format 
  last_edit: <none-or-last-edit-date>, // in YYYY-MM-DDTHH:MM:SS.f format 
  attachments: [    // or empty, if post contains no attachments
    <first-file-id>,
    <second-file-id>,
    ...
  ] 
} 
```

2. create_post (**NOT IMPLEMENTED**)
- URL: /post/create/
- method: POST
- description: <br><br> 
Creates new pos: saves its data to database and saves attached files(for docs on file 
storage structure see [File Storage documentation](#file-storage-documentation) <br> 
AUTHORIZATION is provided by JWT token; post is attached to token owner <br>
REQUEST is expected to have "multipart/form-data" content type, i.e. send data (together with files) in a form format <br>
RESPONSE is {"message": "success"}

About file's storage structure see [File Storage Docs](#file-storage-documentation)

Formdata which will be considered is "title" and "content"; user's id will 
be attached automatically based on JWT-token payload's value. 

3. change_post (**NOT IMPLEMENTED**)
- URL: /post/update/{post_id}/
- method: PUT
- description: <br><br> 
Allows changing post data to post's author (and admin, when functionality is 
implemented in "user" service) <br> 
AUTHORIZATION is provided by JWT token <br> 
REQUEST: valid JSON containing fields to change + files (if any need to be added); if 
files should be deleted, JSON object contains key **"delete_files"**, which value is 
an array of file IDs to be deleted <br>
RESPONSE: is {"message": "success"}

4. fetch_feed (**NOT IMPLEMENTED**)
- URL: /post/feed/
- method: GET
- description: <br><br> 
Forms a feed for user (which is identified via authorization JWT token <br> 
RESPONSE: JSON of following format
```json lines
[
  {
    id: <post_id>,
    title: <post_title>,
    author: <authors_USERNAME>,
    content: <posts-text-content>,
    created_date: <date-of-creatiuon>,  /* in YYYY-MM-DDTHH:MM:SS.f format */
    last_edit: <none-or-last-edit-date>,  /* in YYYY-MM-DDTHH:MM:SS.f format */
    attachments: [
      <file_1_id>,
      <file_2_id>,
      ...
    ]
  },
  {
    id: <post_id>,
    ...
  }
]
```

<br><br>
Random notes: 
- all files by default are available to all users 

### File storage documentation

This application uses NFC (Network File System) in production for storing static files; 

When new post file is accepted for being saved, it's metadata is stored in database table "files"
(you can look its structure in [database documentation](#database-schema)). Most important is that
database stores initial file's name, as it was uploaded.

The directory structure is hash-based for optimizing file lookup on retrieval.

**How file are actually stored?**

Each filename is hashed using [md5 algorithm](https://en.wikipedia.org/wiki/MD5); after that,
file is stored to directory 
```
/<first-two-symbols-of-hash>/<next-two-symbols-of-hash>/
```

with filename```<initial-filename-plus-database-id>.jpg```

EXAMPLE <br>
Let's assume user has downloaded file ```cute_cat.jpg```. It is stored in database, receiving ID 5467.

Hash value of string ```"cute_cat.jpg"``` is ```3c808e77fc1b0aee4435533690be458d```.

So, actual file will be stored in ```/3c/80/cute_cat_5467.jpg```

#### Why is such directory structure used?
To optimize lookup speed - maximum amount of directories in uploads is (26+10)^2=1296; maximum 
amount of each subdirectory is (26+10)^2 as well; If each directory of "second level" stores 1000 
files, we get total of ```1296 * 1296 * 1000 = 1.679.616.000``` files, and don't have to do driect 
lookup of all of them in one place when we need one.

_But why would we hash files instead of simply using filenames?_<br>
Well, to guarantee balanced distribution. If we have 17 million files that start 
with “cute”, we will end up putting 17 million files in the /cu/te directory.

_And why do we add ID on the end of file in end directory?_<br>
To avoid name collision, in case two user will wish to attach ```cute_cat.jpg``` 
pic to their post 

### Database documentation

Chosen database RDBMS is PostgreSQL; database calls are managed via SQLAlchemy
All database-related logic is stored in "/database" directory of the root, which contains 
following files:
- **models.py** - defines all database tables (SQLAlchemy's [models](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models))
- **engine.py** - declares database [engine](https://docs.sqlalchemy.org/en/20/core/connections.html), 
used for connections to the database

#### Database schema

Left blank for now

#### Database migrations

All schema migrations are performed by [alembic](https://alembic.sqlalchemy.org/en/latest/index.html) 
migration tool.

There are three "branches" of migrations (about branches in alembic see [here](https://alembic.sqlalchemy.org/en/latest/branches.html)):
- **main** - performs crucial for an application schema migrations, not violating previous schema's data 
- **dangerous** - performs dangerous operations (i.e. deleting columns, changing constraints, etc.)
> [!CAUTION]
> Before using "dangerous" branch make sure you've read documentation guide related to dangerous operations. 
> (see [lower](#dangerous-migrations))
> 
> Improper dangerous migrations will violate your data!
- **dev** - implements "fixtures" - inserts test users into empty database.
> [!NOTE]
> using "dev" branch is only possible when 
> [POST_DEBUG environment variable](#environment-variables) is set to True and 
> [POST_TESTING env variable](#environment-variables) is set to False

Application code doesn't support interaction with legacy database structure, so developers (if 
they were using previous version and are migrating to new one) are encouraged to perform 
data migrations on their own - for example, using combination of SQLAlchemy and pandas to stream
data in chunks (for example see article [here](https://medium.com/@veligokaysoysaldi/data-migration-with-python-streaming-and-inserting-large-datasets-using-pandas-and-sqlalchemy-in-71a88b7db660))

To launch main database migrations, you should
1. make sure sqlalchemy and alembic dependencies are installed<br>
For that you can just run
```bash
pip install requirements.txt 
```
2. make sure .env file in the root directory of "post" service provides valid credentials for 
connecting to the database (list of requried credentials may be seen [here](#environment-variables))

3. Launch alembic migrations <br>
For that, from the root directory of the service execute
```bash
alembic upgrade main@head 
```

##### Dangerous migrations

All the **dangerous operations**, such are deleting columns/changing column constraints are managed via 
special alembic migration branch - dangerous, and are documented here - in order to ensure that no data 
loss will occure "accidentally", on automatic migrations run. 

> [!CAUTION]
> When migrating database, developers are encouraged to perform dangerous 
> operations (deleting columns, changing column constraints, etc.) cautiously, after 
> properly performing data migration from previous state to the next 

> [!CAUTION]
> before executing dangerous operations, make sure you have acquainted with its nature and
> managed data migration properly

In order to run all the dangerous migrations automatically, from the root directory execute:
```bash
alembic upgrade dangerous@head
```

**_Description of dangerous migrations_**:

1. cabdac6d0430 <br>
when moving from INITIAL to migration #6b9c64dbf3cc<br><br>
DELETES from the table "post" columns:
- "attached_files"
- "author_username" (will be requested from "user" service as needed)


### settings.py module
Module contains all variables, required for normal application workflow variables; 
They are both loaded from environment and are declared inside a file 

**settings.py variables are**:

| Variable | Description |
| -------- | ----------- |
| POSTGRES_USER | represents POSTGRES_USER environment variable |
| POSTGRES_PASSWORD | represents POSTGRES_PASSWORD environment variable |
| PROD_POSTGRES_DB | represents POSTGRES_DB environment variable |
| TEST_POSTGRES_DB | represents TEST_POSTGRES_DB environment variable |
| DB_HOST | represents POSTGRES_HOST environment variable; <br/> localhost if POSTGRES_HOST is not provided |
|||
| FILE_STORAGE_DIRECTORY | defines directory of file storage, related to the root of an application |
|||
| USER_INFO_LINK | represents [USER_INFO_LINK](#environment-variables) environment variable |
|||
| DEBUG | represents [POST_DEBUG](#environment-variables) environment variable; <br/> defaults to False |


### Environment variables

| Variable | Description |
| -------- | ----------- |
| POSTGRES_USER | defines postgres user to access database |
| POSTGRES_PASSWORD | defines password for postgres user |
| POSTGRES_DB | defines name of the **_production_** database on postgres server |
| TEST_POSTGRES_DB | defines name of the **_test_** database on postgres server |
| POSTGRES_HOST | defines HOST for database server |
|||
| NFC_STORAGE_PATH | defines path for mounted Kubernetes PV storage (implemented in [NFC protocol](https://en.wikipedia.org/wiki/Network_File_System) |
|||
| USER_INFO_LINK | defines URL of user service's endpoint, which provides user information on valid auth token <br> |
|||
| POST_DEBUG | states whether an application should run in **debug mode** or not; <br/><br/> DEBUG mode assumes that all required services (redis/celery, etc.) are run on an application startup, not externally in Kubernetes cluster/ Docker Compose file |
| POST_DEBUG_FILE_STORAGE | defines path to file storage when application is run in debug mode (related to the root directory);<br><br> defaults to "/uploads" |
| POST_TESTING | states whether an application is run for testing; <br/><br/> TESTING set to true assumes specifying TEST_POSTGRES_DB variable for successful test run |
