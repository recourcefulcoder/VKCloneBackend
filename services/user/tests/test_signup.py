from database.models import User

from fastapi import status

from httpx import ASGITransport, AsyncClient

import pytest

from sqlalchemy import select

from src.main import app

REGISTER_LINK = "/user/auth/signup"


@pytest.mark.asyncio
async def test_signup_valid_data(session):
    valid_username = "kiric50"
    user_data = {
        "username": valid_username,
        "email": "kiric50@gmail.com",
        "password": "Jungle",
    }
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        response = await client.post(REGISTER_LINK, json=user_data)
    query_res = await session.execute(
        select(User).where(User.username == valid_username)
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user_data
    assert query_res.first() is not None


@pytest.mark.parametrize(
    "data",
    [
        {},
        {
            "password": "valid password",
            "email": "valid@gmail.com",
        },
        {
            "username": "valid username",
            "email": "valid@gmail.com",
        },
        {
            "username": "valid username",
            "password": "valid password",
        },
    ],
)
@pytest.mark.asyncio
async def test_signup_incomplete_data(data):
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        response = await client.post(REGISTER_LINK, json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "email",
    [
        "invalid",
        "invalid@",
        "inva@lid.c",
        "invРУССКИЙalid@gmail.com",
        "inv😊alid@gmail.com",
    ],
)
@pytest.mark.asyncio
async def test_signup_invalid_email(email):
    data = {
        "username": "valid_username",
        "password": "valid password",
        "email": email,
    }
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        response = await client.post(REGISTER_LINK, json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "password",
    [
        "\ttab?",
        "\nnewline",
        "invРУССКИЙ-TEXT",
        "unusual😊symbols",
        "unuÆalÅ",
    ],
)
@pytest.mark.asyncio
async def test_signup_invalid_password(password):
    data = {
        "username": "valid_username",
        "password": password,
        "email": "valid_email@gmail.com",
    }
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        response = await client.post(REGISTER_LINK, json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
