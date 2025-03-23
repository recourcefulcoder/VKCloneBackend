import asyncio
import datetime

from fastapi import status

from httpx import ASGITransport, AsyncClient

import pytest

import pytest_asyncio

from src.auth import TokenManager, generate_jwt_token, generate_refresh_token
from src.main import app

import testvars

from . import pytestmark

USER_ID = testvars.USER_IDS[0]
REFRESH_LINK = app.url_path_for("refresh")


@pytest_asyncio.fixture
async def token():
    refresh_token = generate_refresh_token(USER_ID)
    await TokenManager().set_refresh(USER_ID, refresh_token)
    yield refresh_token
    await TokenManager().delete_refresh(USER_ID)


async def test_valid_refresh(token):
    async with AsyncClient(
        transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
    ) as client:
        response = await client.post(
            REFRESH_LINK, json={"refresh_token": token}
        )

    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert "refresh_token" in data.keys()
    assert "access_token" in data.keys()


async def test_expired_refresh():
    exp_refresh = generate_jwt_token(USER_ID, datetime.timedelta(seconds=1))
    await TokenManager().set_refresh(USER_ID, exp_refresh)
    await asyncio.sleep(1)
    async with AsyncClient(
        transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
    ) as client:
        response = await client.post(
            REFRESH_LINK, json={"refresh_token": exp_refresh}
        )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "refresh",
    [
        "INVALID",
        generate_refresh_token(USER_ID),  # since not added to Redis
    ],
)
async def test_invalid_refresh(refresh):
    async with AsyncClient(
        transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
    ) as client:
        response = await client.post(
            REFRESH_LINK, json={"refresh_token": refresh}
        )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# @pytest_asyncio.fixture
# async def deleted_user_refresh(session, client):
#     # client is imported to initialize application
#     # before test startapp - otherwise SQLAlchemy's listeners won't
#     # be attached
#     new_user_id = testvars.USERS_AMOUNT + 1
#     await session.execute(
#         insert(User)
#         .values(
#             username="valid_username",
#             _password=User.hash_password("valid_password"),
#             email="new_valid_email@gmail.com",
#         )
#     )
#     refresh = generate_refresh_token(new_user_id)
#     await TokenManager().set_refresh(new_user_id, refresh)
#     await session.execute(
#         delete(User)
#         .where(User.id == new_user_id)
#     )
#     yield refresh
#
#
# async def test_deleted_user_refresh(deleted_user_refresh, client):
#     response = await client.post(
#         REFRESH_LINK, json={"refresh_token": deleted_user_refresh}
#     )
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
