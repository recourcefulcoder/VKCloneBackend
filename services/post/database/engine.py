import settings

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

DB_NAME = (
    settings.TEST_POSTGRES_DB
    if settings.TESTING
    else settings.PROD_POSTGRES_DB
)

url_object = URL.create(
    "postgresql+asyncpg",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.DB_HOST,
    database=DB_NAME,
)

engine = create_async_engine(url_object, poolclass=NullPool)
