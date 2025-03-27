from database.engine import engine
from database.models import File, Post

from httpx import ASGITransport, AsyncClient

import pytest_asyncio

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.main import app

from . import testvars


@pytest_asyncio.fixture
async def session():
    async with async_sessionmaker(engine)() as session1:
        yield session1
        await session1.rollback()


@pytest_asyncio.fixture(scope="session")
async def setup_session():
    async with async_sessionmaker(engine)() as session1:
        yield session1


async def add_test_data(session: AsyncSession):
    post = Post(
        id=testvars.POST_DATA["id"],
        title=testvars.POST_DATA["title"],
        content=testvars.POST_DATA["content"],
        author_id=testvars.POST_DATA["author_id"],
        creation_date=testvars.POST_DATA["creation_date"],
        last_edit=testvars.POST_DATA["last_edit"],
    )
    session.add(post)
    await session.commit()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _add_data(setup_session):
    await add_test_data(setup_session)
    yield


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _delete_data(setup_session):
    yield
    await setup_session.execute(delete(Post))
    await setup_session.execute(delete(File))
    await setup_session.commit()


@pytest_asyncio.fixture
async def _rollback_any_changes(session):
    yield
    await session.execute(delete(Post))
    await session.execute(delete(File))
    await add_test_data(session)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
    ) as client1:
        yield client1
