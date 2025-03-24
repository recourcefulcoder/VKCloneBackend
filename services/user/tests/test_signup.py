from database.models import User

from fastapi import status

import pytest

import pytest_asyncio

from sqlalchemy.sql import delete, select

from . import pytestmark, testvars

REGISTER_LINK = "/user/auth/signup"


@pytest_asyncio.fixture(autouse=True)
async def _delete_odd_users(session):
    yield
    await session.execute(
        delete(User).where(User.id.not_in(testvars.USER_IDS))
    )
    await session.commit()


async def test_signup_valid_data(session, client):
    valid_username = "kiric50"
    user_data = {
        "username": valid_username,
        "email": "kiric50@gmail.com",
        "password": "Jungle",
    }
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
async def test_signup_incomplete_data(data, client):
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
async def test_signup_invalid_email(email, client):
    data = {
        "username": "valid_username",
        "password": "valid password",
        "email": email,
    }
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
async def test_signup_invalid_password(password, client):
    data = {
        "username": "valid_username",
        "password": password,
        "email": "valid_email@gmail.com",
    }
    response = await client.post(REGISTER_LINK, json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
