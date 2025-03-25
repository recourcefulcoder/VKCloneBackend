import settings

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

url_object = URL.create(
    "postgresql+asyncpg",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.DB_HOST,
    database=settings.POSTGRES_DB,
)

engine = create_async_engine(url_object, poolclass=NullPool)
