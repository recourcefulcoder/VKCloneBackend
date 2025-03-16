# USER service of VKCloneBackend

This document contains code documentation for the USER service 

Table of contents:
- [Environment variables used](#environment-variables)
- [Documentation](#documentation)
  - [Endpoint handlers docs](#endpoints) 

## Environment variables

In order for this server to function properly, environment must have following variables 
specified:

| variable name | carried value |
| ------------- | ------------- |
| DB_HOST | name of host handling database requests; defaults to _localhost_|
| POSTGRES_USER | name of PostgreSQL database user to be used for connections|
| POSTGRES_PASSWORD | password for POSTGRES_USER |
| POSTGRES_DB | name of PostgreSQL DB for the service |


## Documentation

/src files and their contents 
- pydmodels.py - contains Pydantic models, used for request validation in FastAPI request handlers
- main.py - contains main application logic - defined FastAPI app instance, handlers declared, etc.

### Endpoints

#### /signup endpoint
Data validation is processed both via Pydantic model and SQLAlchemy's model validation.
**Pydantic** ensures data is passed, **SQLAlchemy's model validators** - that data is valid;

For that user instance is created and wrapped in try-except, which handles ValueError raising.
