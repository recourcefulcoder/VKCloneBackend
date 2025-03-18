import subprocess

import config

from database.engine import engine
from database.models import User

import pytest

import pytest_asyncio

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker

import testvars


@pytest_asyncio.fixture
async def session():
    async with async_sessionmaker(engine)() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def _delete_odd_users(session):
    yield
    await session.execute(
        delete(User).where(User.id.not_in(testvars.USER_IDS))
    )
    await session.commit()


@pytest.fixture(autouse=True, scope="session")
def run_redis_if_needed():
    proc = None
    if config.DEBUG:
        proc = subprocess.Popen("redis-server --port 6379", shell=True)
    yield
    if config.DEBUG:
        proc.kill()
