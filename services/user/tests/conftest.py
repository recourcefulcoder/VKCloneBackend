from asgi_lifespan import LifespanManager

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
def _run_services_if_needed():
    proc = []
    # if config.DEBUG:
    #     proc.append(
    #         subprocess.Popen(
    #             "celery -A src.celery_app worker --loglevel=info", shell=True
    #         )
    #     )
    #     sleep(2)  # give services time for startup
    yield
    for pr in proc:
        pr.kill()


@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
        ) as async_client:
            yield async_client
