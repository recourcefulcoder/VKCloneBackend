import os

from shared.utils import load_environ

load_environ()

DB_HOST = os.getenv("DB_HOST", default="localhost")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
