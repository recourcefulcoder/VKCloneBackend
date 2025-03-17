![tests](https://github.com/recourcefulcoder/VKCloneBackend/actions/workflows/user-tests.yml/badge.svg)

# USER service of VKCloneBackend

This document contains code documentation for the USER service 

Table of contents:
- [Running in dev mode](#running-service-in-developer-mode)
- [Notes on testing](#testing) (**MUST-READ** before launching!)
- [Documentation](#documentation)
  - [Environment variables used](#environment-variables)
  - [Project general structure](#project-structure) 
  - [Database models](#database-models-user-model) 
  - [Endpoint handlers docs](#endpoints) 

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

3. Update PYTHONPATH with root directory of the project and root directory of the service

To do that in Linux, run
```bash
export PYTHONPATH="path/to/root/dir:path/to/root/dir/services/<service_name>:$PYTHONPATH"
```
4. Create PostgreSQL database and migrate with alembic

Create a PostgreSQL service, provide valid credentials for it in .env file (see above)
and migrate it using alembic. From the root directory of service, run:

```bash
alembic upgrade main@head
```

5. Run FastAPI

From "src" directory of the service run
```bash
fastapi dev main.py
``` 

6. _Enjoy ^\_^_

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
Preferred, yet not supported currently variant

### Manual running instructions
1. Create a test PostgreSQL database
2. Provide credentials for connecting to TEST database in .env file

> [!CAUTION]
> Not paying enough attention on this step WILL violate data in your DEV/PROD database, so 
> make sure to provide credentials for TEST database!!

3. Run database migrations via alembic

For that, run from the root directory of the service:
```bash
alembic upgrade test@head
```
4. Install test dependencies

They are listed in test-req.txt file; you can install them with
```bash
pip install -r test-req.txt 
```

5. Run tests with pytest

From the root directory of the project execute
```bash
pytest tests
```

## Documentation

### Environment variables

In order for this server to function properly, environment must have following variables 
specified:

| variable name | carried value |
| ------------- | ------------- |
| DB_HOST | name of host handling database requests; defaults to _localhost_|
| POSTGRES_USER | name of PostgreSQL database user to be used for connections|
| POSTGRES_PASSWORD | password for POSTGRES_USER |
| POSTGRES_DB | name of PostgreSQL DB for the service |

### Project structure

/src files and their contents
- pydmodels.py - contains Pydantic models, used for request validation in FastAPI request handlers
- main.py - contains main application logic - defined FastAPI app instance and "user" router registration
- dependencies.py - contains app dependencies to be included

Main logic of the application (meaning endpoint handlers) is defined in routers/users.py

### Database models (User model)

It was decided to stick to separate ORM logic and data validation (via Pydantic) for security 
reasons - in order not to expose unintentionally some sensitive user information in API returns.

So the model is declared using SQLAlchemy.

Password is automatically hashed on user creation - since that, password validation on 
user creation/update must be done outside from SQLAlchemy ORM model (via Pydantic models, for example)

### Endpoints

#### /signup endpoint
Data validation is given to Pydantic model, yet SQLAlchemy's User model still contains email validation (just in case)
