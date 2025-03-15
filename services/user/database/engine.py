import os

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool


url_object = URL.create(
    "postgresql+asyncpg",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("DB_HOST", default="localhost"),
    database=os.getenv("POSTGRES_DB"),
)
engine = create_async_engine(url_object, poolclass=NullPool)
