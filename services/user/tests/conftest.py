import subprocess

import config

from database.engine import engine

import pytest

import pytest_asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker


@pytest_asyncio.fixture
async def session():
    async with async_sessionmaker(engine)() as session:
        yield session


@pytest.fixture(autouse=True, scope="session")
def run_redis_if_needed():
    proc = None
    if config.DEBUG:
        proc = subprocess.Popen("redis-server --port 6379", shell=True)
    yield
    if config.DEBUG:
        proc.kill()
