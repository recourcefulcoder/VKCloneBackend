![tests](https://github.com/recourcefulcoder/VKCloneBackend/actions/workflows/post-tests.yml/badge.svg)

# POST service of VKCloneBackend


Table of contents:
---
- [End goal description]()
- [Launching application](#running-an-application)
  - [In dev mode](#running-application-manually-so-called-in-dev-mode) (manually)
  - [With Docker Compose]()
- [Notes on testing](#testing-notes) (**MUST READ** before launching)
- [Documentation](#documentation)
  - [Database](#database-documentation)
    - [Database migrations](#database-migrations)
  - [settings.py module](#settingspy-module)
  - [Environment variables](#environment-variables) 

## End goal outline
This section defines complete list of requirements for the service - endpoints implemented,
architectural decisions made, connections with other services (Redis, PostgreSQL, executive services, etc.)

Endpoints table
1. get_files (**NOT IMPLEMENTED**)
   - URL: /post/files?id=...
- method: GET
- description: <br><br>
requests files with IDs, provided in request URL, gets files returned <br>
RESPONSE: requested files<br><br>
URL example (requests files with ids 12, 45 and 54): 
```
/post/files?id=12&id=45&id=54
```

2. get_post (**NOT IMPLEMENTED**)
- URL: /post/get/{post_id}/
- method: GET
- description: <br><br>
Returns information about single post with ID post_id; <br>
REQUEST is done via GraphQL standard <br> RESPONSE is a valid JSON, containing requested info

3. create_post (**NOT IMPLEMENTED**)
- URL: /post/create/
- method: POST
- description: <br><br> 
Creates new post; <br> 
AUTHORIZATION is provided by JWT token; post is attached to token owner <br>
REQUEST is a valid JSON, containing all required fields + files that need to be attached to that post
RESPONSE is {"message": "success"}

4. change_post (**NOT IMPLEMENTED**)
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

5. fetch_feed (**NOT IMPLEMENTED**)
- URL: /post/feed/
- method: GET
- description: <br><br> 
Forms a feed for user (which is identified via authorization JWT token <br> 
RESPONSE: JSON of following format
```json lines
[
  {
    id: <post_id>,
    author: <authors_USERNAME>,
    content: <post_text_context>,
    created_date: <created_date>  /* in YYYY-MM-DDTHH:MM:SS.f format */
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

3. Update PYTHONPATH with root directory of the service

To do that in Linux, run
```bash
export PYTHONPATH="path/to/root/dir/services/<service_name>:$PYTHONPATH"
```
4. Create PostgreSQL database and migrate with alembic

Create a PostgreSQL service, provide valid credentials for it in .env file (see above)
and migrate it using alembic. From the root directory of service, run:

```bash
alembic upgrade main@head
```

6. Run FastAPI

From "src" directory of the service run
```bash
fastapi dev main.py
``` 

7. _Enjoy ^\_^_


### Running with Docker Compose
Not implemented yet

## Testing notes
Empty for now

## Documentation

### Database documentation

Chosen database RDBMS is PostgreSQL; database calls are managed via SQLAlchemy
All database-related logic is stored in "/database" directory of the root, which contains 
following files:
- **models.py** - defines all database tables (SQLAlchemy's [models](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models))
- **engine.py** - declares database [engine](https://docs.sqlalchemy.org/en/20/core/connections.html), 
used for connections to the database

#### Database migrations

All schema migrations are performed by [alembic](https://alembic.sqlalchemy.org/en/latest/index.html) 
migration tool.

All the **dangerous operations**, such are deleting columns/changing column constraints are managed via 
special alembic migration branch - dangerous, and are documented here - in order to ensure that no data loss will occure "accidentally", on
automatic migrations run. 

> [!CAUTION]
> When migrating database, developers are encouraged to perform dangerous 
> operations (deleting columns, changing column constraints, etc.) cautiously, after 
> properly performing data migration from previous state to the next 

Application code doesn't support interaction with legacy database structure, so developers (if 
they were using previous version and are migrating to new one) are encouraged to perform 
data migrations on their own - for example, using combination of SQLAlchemy and pandas to stream
data in chunks (see article [here](https://medium.com/@veligokaysoysaldi/data-migration-with-python-streaming-and-inserting-large-datasets-using-pandas-and-sqlalchemy-in-71a88b7db660))

To launch database migrations, you should
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

##### Dangerous migrations:
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
| POSTGRES_DB | represents POSTGRES_DB environment variable |
| DB_HOST | represents POSTGRES_HOST environment variable; <br/> localhost if POSTGRES_HOST is not provided |
|||
| DEBUG | represents [POST_DEBUG](#environment-variables) environment variable; <br/> defaults to False |


### Environment variables

| Variable | Description |
| -------- | ----------- |
| POSTGRES_USER | defines postgres user to access database |
| POSTGRES_PASSWORD | defines password for postgres user |
| POSTGRES_DB | defines name of the database on postgres server |
| POSTGRES_HOST | defines HOST for database server |
|||
| POST_DEBUG | states whether an application should run in **debug mode** or not; <br/><br/> DEBUG mode assumes that all required services (redis/celery, etc.) are run on an application startup, not externally in Kubernetes cluster/ Docker Compose file|
