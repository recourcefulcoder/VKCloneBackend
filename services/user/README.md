![tests](https://github.com/recourcefulcoder/VKCloneBackend/actions/workflows/user-tests.yml/badge.svg)

# USER service of VKCloneBackend

This document contains code documentation for the USER service 

Table of contents:
- [Running in dev mode](#running-service-in-developer-mode)
- [Debug application mode](#debug-mode)
- [Notes on testing](#testing) (**MUST-READ** before launching!)
- [Dockerization]()
- [Documentation](#documentation)
  - [Environment variables used](#environment-variables)
  - [Project general structure](#project-structure) 
    - [Project configuration in config.py](#configpy-file) 
  - [Database models](#database-models-user-model) 
  - [Endpoint handlers docs](#endpoints) 
  - [Authorization utils](#authorization-utils-authpy)

## Running service in developer mode

1. Install dependencies

From root directory of the "user" service execute in your system's CLI and switch to "/src" directory:
```bash
pip install -r requirements.txt
cd src
```

2. Create .env file

User service (just as any service, actually) requires some environment variables for 
its valid work, which are described in its README.md file.
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

5. Set up a Redis server (or specify running mode as DEBUG by setting 
[USER_DEBUG=True](#environment-variables) in your .env file)

6. Run FastAPI

From "src" directory of the service run
```bash
fastapi dev main.py
``` 

7. _Enjoy ^\_^_

## Debug mode
Debug mode is a special runmode where service is run on its own, without any other services attached to it.
Applciation runs in DEBUG when USER_DEBUG environment variable is set to one of these values: 
- True
- yes
- y
- 1

What are main differences to prod/dev mode?
- It spams Redis service on its own via [subprocess](https://docs.python.org/3/library/subprocess.html) 
python module 

And that's it for now. Yet It is not ruled out this section will expand with time.

## Testing
Since tests may perform CRUD operations on a database, they need an isolated database for runtime.
This may be achieved in two ways - either manually via providing credentials for TEST database in 
.env file or via running tests in test Docker container (not supported currently)

Once more
> [!CAUTION]
> DO NOT run tests on your production/development database, as they MOST DEFINITELY will
> violate data in them. Take care of providing credentials for TEST database in .env file 
> when running tests manually

### Word about test migration
Test migration creates two test users:
1. kiric 
    - id: 1
    - email: valid@gmail.com
    - password: Harmonica52
2. mimic 
    - id: 2
    - email: "valid2@gmail.com"
    - password: Harmonica52

These two are used for testing auth endpoints.

### Running with Docker instructions
Preferred since is safer and easier to run

In order to run tests, execute from the root directory of the service:
```bash
docker compose up --build -d
docker exec user-service pytest
```
(replacing **_user-service_** with actual name of service container running; 
yet it truly is the name of the container by default )

In order to delete container after test execution, run following command:
```bash
docker compose down -v
```

### Manual running instructions
1. Create and set up a test PostgreSQL database
2. Create and set up Redis DB (or set [USER_DEBUG env variable](#environment-variables) to 
True to ask pytest to spam Redis process himself)
3. Provide credentials for connecting to TEST database in .env file

> [!CAUTION]
> Not paying enough attention on this step WILL violate data in your DEV/PROD database, so 
> make sure to provide credentials for TEST database!!

4. Run database migrations via alembic

For that, run from the root directory of the service:
```bash
alembic upgrade test@head
```
5. Install test dependencies

They are listed in test-req.txt file; you can install them with
```bash
pip install -r test-req.txt 
```

6. Run tests with pytest

From the root directory of the project execute
```bash
pytest tests
```

## Dockerization
Even though project has Dockerfile, it is not yet considered to be valid Docker, as it is aimed for tests:
- creates test data in the database
- contains **_DANGEROUS_** test package (which violates database data on runtime, see [testing](#testing))

As another testing mechanism will be implemented, it will be possible to use same Dockerfile for 
blueprinting prod-like Docker image; for now it requires following adjustments:
- add /tests to .dockerignore
- edit entrypoint.sh: rewrite line which runs database migrations to 
```bash
alembic upgrad main@head
```

## Documentation

### Environment variables

In order for this server to function properly, environment must have following variables 
specified:

| variable name | carried value |
| ------------- | ------------- |
| DB_HOST | name of host associated with PostgreSQL DB; defaults to _localhost_|
| REDIS_HOST | name of host associated with Redis DB; defaults to _localhost_|
|||
| POSTGRES_USER | name of PostgreSQL database user to be used for connections|
| POSTGRES_PASSWORD | password for POSTGRES_USER |
| POSTGRES_DB | name of PostgreSQL DB for the service |
|||
| USER_DEBUG | defines whether application is running in debug mode or not; _False_ by default |

### Project structure

/src files and their contents
- **main.py** - contains main application logic - defined FastAPI app instance and "user" router registration
- **auth.py** - contains authorization-related logic, meaning TokenManager class 
(handling redis operations) and token-manipulation functions (creation/verification)
- **dependencies.py** - contains app dependencies to be included
- **pydmodels.py** - contains Pydantic models, used for request validation in FastAPI request handlers

Main logic of the application (meaning endpoint handlers) is defined in routers/users.py

#### config.py file

This file is stored in the root directory of the project and contains all essential setting 
variables of the project (consider it to be a copy of [setting.py](https://docs.djangoproject.com/en/5.1/topics/settings/) 
module in Django)

It is stored in the root directory of the project.

Variables of config.py:

| Variable | Value and function |
| -------- | ------------------ |
| DB_HOST | represents DB_HSOT env variable |
| POSTGRES_USER | represents POSTGRES_USER env variable |
| POSTGRES_PASSWORD | represents POSTGRES_PASSWORD env variable |
| POSTGRES_DB | represents POSTGRES_DB env variable |
| JWT_SECRET_KEY| represents JWT_SECRET_KEY env variable |
| DEBUG | represents USER_DEBUG env variable |
|||
| JWT_ALGORITHM | stores algorithm for JWT-token payload encoding/decoding |
| ACCESS_EXP_TIME | datetime.timedelta object, representing **access token** lifetime |
| REFRESH_EXP_TIME | datetime.timedelta object, representing **refresh token** lifetime |


### Database models (User model)

It was decided to stick to separate ORM logic and data validation (via Pydantic) for security 
reasons - in order not to expose unintentionally some sensitive user information in API returns.

So the model is declared using SQLAlchemy.

Password is automatically hashed on user creation - since that, password validation on 
user creation/update must be done outside from SQLAlchemy ORM model (via Pydantic models, for example)

### Endpoints

Currently two (2) routers are implemented for an application:
- Basic one: adding "/user" prefix to all the endpoints
- Authorization: adding "/auth" prefix, handles signup/signin

#### auth/signup endpoint
Data validation is given to Pydantic model, yet SQLAlchemy's User model still contains email validation (just in case)
Processes request, containing necessarily fields "username", "email", "password" which should pass the validation

- password: only ASCII letters, digits and specials symbols from the list: !@#$%^&*()_+?=\-"'<>,./\|{}[]:;`~
- email: valid email (containts @, must have domain, subdomain contains at least two character, 
allowed only ASCII letters, digits and some special symbols, such are ._%+- )

#### auth/login endpoint

Processes sent form data with credentials, returns [JWT-tokens](https://jwt.io/introduction) 
on valid credentials.

User authorization protocol used is OAuth2 with password flow; 

OAuth2 specifies that when using the "password flow" (that is used here) the client/user 
must send a username and password fields as form data - so required fields on this endpoint are
packed in form data "password" and "username".

Form data requirements:
- should contain "password" keyword
- should contain "username" keyword 

Return json object contains following keys:
- access_token - access JWT-token
- refresh_token - refresh JWT-token

#### auth/refresh endpoint
Processes JWT-token refreshment; accepts refresh_token in request data, returns a new pair of 
refresh and access tokens (+ deletes old/adds new refresh token to Redis)

Payload requirements:
- must contain key "refresh_token" 

### Authorization utils (auth.py)
#### TokenManager class 
This class is basically a wrapper of redis-py asynchronous Redis class
(see examples of usage [here](https://redis-py.readthedocs.io/en/latest/connections.html)),
created in order to ensure singleton implementation (meaning to ensure that redis dependency always accesses same
instance of Redis client) and implement API for writing/reading/deleting _refresh tokens_ from the Redis DB

Created in a singleton pattern, in order not to overcome Redis' TCP-connection limit 
(since each new object would open new TCP connection), and each new instance would use 
separate connection pool, which practically disables any performance upscales related to pooling connections

----------
Class attributes:
- **_redis** - defines asynchronous redis client; 
-----------
Class methods:

There are two groups of this class' methods:
1. These are mirroring [redis-py commands](https://redis-py.readthedocs.io/en/latest/commands.html).
in order to provide API without accessing **_redis** instance directly
- async def setex - mirroring Redis instance's method setex
- async def get - mirroring Redis instance's method get
- async def deletes - mirroring Redis instance's method get
2. Refresh token-specific
- async def get_refresh(user_id: int) - returns refresh token for user with ID user_id; 
returns None if not found or str (value of refresh) if found
- async def delete_refresh(user_id: int) - deletes refresh token for user with ID user_id
- async def set_refresh(self, user_id: int, refresh: str) - sets a refresh for user on key "refresh_token:<user_id>"


#### Token-related functions
- generate_access_token(email: str) - generates JWT access token, based on email provided.

**sub value** of JWT payload is chosen to be a user's id

**expiry time** is decided based on value of ACCESS_EXPIRY_TIME value in [config.py](#configpy-file)
- decode_access_token(token: str) - decodes JWT-token value passed;

_**Return value**_: if invalid (invalid format/expired/unable to decode) returns None; if valid, 
returns content of "sub" key of the payload (i.e. user's email); 
> [!WARNING]
> It doesn't check email on validity/presence in database - it only decodes given token string, and that's it 
