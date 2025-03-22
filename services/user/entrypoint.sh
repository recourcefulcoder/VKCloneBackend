#!/usr/bin/env sh

alembic upgrade main@head
cd src
fastapi run main.py