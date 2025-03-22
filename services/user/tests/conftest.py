import subprocess

import config

from database.engine import engine

from httpx import ASGITransport, AsyncClient

import pytest

import pytest_asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.main import app

from . import testvars


@pytest_asyncio.fixture
async def session():
    async with async_sessionmaker(engine)() as session:
        yield session


@pytest.fixture(autouse=True, scope="session")
def _run_redis_if_needed():
    proc = None
    if config.DEBUG:
        proc = subprocess.Popen("redis-server --port 6379", shell=True)
    yield
    if config.DEBUG:
        proc.kill()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
    ) as async_client:
        yield async_client
