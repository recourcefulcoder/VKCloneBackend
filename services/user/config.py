import datetime
import os

from src.utils import load_environ


def load_local_and_global_environ():
    load_environ()
    load_environ(depth=1)


load_local_and_global_environ()


DB_HOST = os.getenv("DB_HOST", default="localhost")
REDIS_HOST = os.getenv("REDIS_HOST", default="localhost")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"

ACCESS_EXP_TIME = datetime.timedelta(minutes=15)
REFRESH_EXP_TIME = datetime.timedelta(days=14)

DEBUG = os.getenv("USER_DEBUG", default="False").lower() in [
    "true",
    "yes",
    "y",
    "1",
]
