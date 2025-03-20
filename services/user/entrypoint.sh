#!/usr/bin/env sh

alembic upgrade test@head
cd src
fastapi run main.py