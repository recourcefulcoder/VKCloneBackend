![tests](https://github.com/recourcefulcoder/VKCloneBackend/actions/workflows/post-tests.yml/badge.svg)

# POST service of VKCloneBackend

Table of contents:
- Launching application
  - [In dev mode](#running-application-manually-so-called-in-dev-mode) (manually)
  - [With Docker Compose]()
- Notes on testing (**MUST READ** before launching)
- [Documentation](#documentation)
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
| POST_DEBUG | states whether an application should run in **debug mode** or not; <br/><br/> DEBUG mode assumes that all required services (redis/celery, etc.) are run on an application startup, not externally in Kubernetes cluster/ Docker Compsoe file|
