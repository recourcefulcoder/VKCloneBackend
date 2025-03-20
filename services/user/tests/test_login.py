from database.models import User

from fastapi import status

from httpx import ASGITransport, AsyncClient

import pytest

from sqlalchemy.sql import select

from src.auth import TokenManager
from src.main import app

import testvars


LOGIN_LINK = app.url_path_for("login")


@pytest.mark.parametrize(
    "payload",
    [
        {
            "username": testvars.USER1_USERNAME,
            "password": testvars.USER1_PASSWORD,
        },
        {
            "username": testvars.USER2_USERNAME,
            "password": testvars.USER2_PASSWORD,
        },
    ],
)
@pytest.mark.asyncio
async def test_valid_credentials(payload):
    async with AsyncClient(
        transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
    ) as client:
        response = await client.post(
            LOGIN_LINK,
            data=payload,
        )
    response_content = response.json().keys()
    assert response.status_code == status.HTTP_200_OK
    assert "refresh_token" in response_content
    assert "access_token" in response_content


@pytest.mark.parametrize(
    "payload",
    [
        {
            "password": "validPassword",
        },
        {
            "username": testvars.USER1_USERNAME,
        },
        {
            "email": testvars.USER1_EMAIL,
        },
        {},
    ],
)
@pytest.mark.asyncio
async def test_incomplete_credentials(payload):
    async with AsyncClient(
        transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
    ) as client:
        response = await client.post(
            LOGIN_LINK,
            data=payload,
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "payload",
    [
        {
            "username": testvars.USER1_USERNAME,
            "password": testvars.USER1_PASSWORD + "invalid_add",
        },
        {
            "username": testvars.USER1_USERNAME + "invalid_add",
            "password": testvars.USER1_PASSWORD,
        },
    ],
)
@pytest.mark.asyncio
async def test_invalid_credentials(payload):
    async with AsyncClient(
        transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
    ) as client:
        response = await client.post(
            LOGIN_LINK,
            data=payload,
        )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_non_existing_user():
    payload = {
        "username": f"INVALID_{testvars.USER1_USERNAME}_INVALID",
        "password": "valid",
    }
    async with AsyncClient(
        transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
    ) as client:
        response = await client.post(
            LOGIN_LINK,
            data=payload,
        )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_malicious_input_defence(session):
    payload = {
        "username": f"TRUNCATE TABLE {User.__tablename__};",
        "password": "valid_password",
    }
    async with AsyncClient(
        transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
    ) as client:
        response = await client.post(
            LOGIN_LINK,
            data=payload,
        )
    users = await session.execute(select(User))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert users.first() is not None


@pytest.mark.asyncio
async def test_refresh_updated():
    valid_payload = {
        "username": testvars.USER1_USERNAME,
        "password": testvars.USER1_PASSWORD,
    }
    async with AsyncClient(
            transport=ASGITransport(app), base_url=testvars.TEST_BASE_URL
    ) as client:
        response = await client.post(
            LOGIN_LINK,
            data=valid_payload,
        )
        prev_token = response.json()["refresh_token"]
        await client.post(
            LOGIN_LINK,
            data=valid_payload,
        )
    assert await TokenManager().get_refresh(1) != prev_token
