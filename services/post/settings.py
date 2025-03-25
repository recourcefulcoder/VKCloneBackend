import os

from src.utils import load_environ


def load_local_and_global_environ():
    load_environ()
    load_environ(depth=1)


load_local_and_global_environ()

DEBUG = os.getenv("POST_DEBUG", default="false").lower() in [
    "true",
    "yes",
    "y",
    "1",
]

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DB_HOST = os.getenv("POSTGRES_HOST", default="localhost")
