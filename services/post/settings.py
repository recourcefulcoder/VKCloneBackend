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
TESTING = os.getenv("POST_TESTING", default="false").lower() in [
    "true",
    "yes",
    "y",
    "1",
]

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PROD_POSTGRES_DB = os.getenv("POSTGRES_DB")
TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB")

DB_HOST = os.getenv("POSTGRES_HOST", default="localhost")

NFC_STORAGE_PATH = os.getenv("NFC_STORAGE_PATH")

FILE_STORAGE_DIRECTORY = (
    os.getenv("POST_DEBUG_FILE_STORAGE", default="/uploads")
    if DEBUG
    else NFC_STORAGE_PATH
)
