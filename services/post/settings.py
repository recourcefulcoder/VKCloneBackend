import logging
import os
import sys

from src.utils import load_environ


logger = logging.getLogger(__name__)


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
if FILE_STORAGE_DIRECTORY is None:
    add_message = (
        "Maybe you forgot to define " "NFC_STORAGE_PATH environment variable?"
    )
    logger.error(
        "Improperly configured: "
        "file storage directory not specified. " + add_message
    )
    sys.exit(1)

USER_INFO_LINK = os.getenv("USER_INFO_LINK")

if USER_INFO_LINK is None:
    logger.error(
        "Improperly configured: USER_INFO_LINK "
        "environment variable not specified"
    )
    sys.exit(1)
