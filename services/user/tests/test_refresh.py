import asyncio
import datetime

from fastapi import status

from httpx import ASGITransport, AsyncClient

import pytest

import pytest_asyncio

from src.auth import TokenManager, generate_jwt_token, generate_refresh_token
from src.main import app

import testvars


USER_ID = testvars.USER_IDS[0]
REFRESH_LINK = app.url_path_for("refresh")


@pytest_asyncio.fixture
async def token():
    refresh_token = generate_refresh_token(USER_ID)
    await TokenManager().set_refresh(USER_ID, refresh_token)
    yield refresh_token
    await TokenManager().delete_refresh(USER_ID)


@pytest.mark.asyncio
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


@pytest.mark.asyncio
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
    ]
)
@pytest.mark.asyncio
async def test_invalid_refresh(refresh):
    async with AsyncClient(
        transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
    ) as client:
        response = await client.post(
            REFRESH_LINK, json={"refresh_token": refresh}
        )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
