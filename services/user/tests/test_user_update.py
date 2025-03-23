from datetime import timedelta

from database.engine import engine
from database.models import User

from fastapi import status

import pytest

import pytest_asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.sql import delete, insert, select, update

from src.auth import generate_access_token, generate_jwt_token
from src.main import app

import testvars

from . import pytestmark


UPDATE_USER_ID = testvars.USERS_AMOUNT + 1
UPDATE_USER_USERNAME = "update_user_username"
UPDATE_USER_PASSWORD = "valid_password"
UPDATE_USER_EMAIL = "update_user_valid@gmail.com"
UPDATE_URL = app.url_path_for("update_user")


@pytest_asyncio.fixture(scope="module")
async def module_session():
    async with async_sessionmaker(engine)() as session:
        yield session


@pytest_asyncio.fixture(scope="module", autouse=True)
async def _create_updatable_user(module_session):
    await module_session.execute(
        insert(User).values(
            id=UPDATE_USER_ID,
            _password=User.hash_password(UPDATE_USER_PASSWORD),
            email=UPDATE_USER_EMAIL,
            username=UPDATE_USER_USERNAME,
        )
    )
    await module_session.commit()


@pytest_asyncio.fixture(autouse=True)
async def _set_user_to_default(session):
    yield
    await session.execute(
        update(User)
        .where(User.id == UPDATE_USER_ID)
        .values(
            id=UPDATE_USER_ID,
            _password=User.hash_password(UPDATE_USER_PASSWORD),
            email=UPDATE_USER_EMAIL,
            username=UPDATE_USER_USERNAME,
        )
    )
    await session.commit()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def _delete_update_user(module_session):
    yield
    await module_session.execute(delete(User).where(User.id == UPDATE_USER_ID))
    await module_session.commit()


async def test_updates_on_valid(client, session):
    payload = {
        "username": "hihihiha",
    }
    response = await client.put(
        UPDATE_URL,
        json=payload,
        headers={
            "Authorization": f"Bearer {generate_access_token(UPDATE_USER_ID)}"
        },
    )
    resp_data = response.json()
    resq = await session.execute(select(User).where(User.id == UPDATE_USER_ID))
    user = resq.scalar()
    assert response.status_code == status.HTTP_200_OK
    assert resp_data["username"] == payload["username"]
    assert user.username == payload["username"]


@pytest.mark.parametrize(
    "token",
    [
        "invalid",
        "",
        generate_access_token(UPDATE_USER_ID + 1),  # not existing user
        generate_jwt_token(UPDATE_USER_ID, timedelta(minutes=-1)),
    ],
)
async def test_401_on_invalid_token(token, client):
    valid_payload = {"username": "new_username"}
    response = await client.put(
        UPDATE_URL,
        json=valid_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_returns_valid_fields(client):
    valid_payload = {"username": "new_username"}
    response = await client.put(
        UPDATE_URL,
        json=valid_payload,
        headers={
            "Authorization": f"Bearer {generate_access_token(UPDATE_USER_ID)}"
        },
    )
    keys = response.json().keys()
    required = ["id", "username", "email", "created_date"]
    assert all(key in keys for key in required)
    assert len(keys) == len(required)  # only required are returned


async def test_updates_password(client, session):
    new_pass_payload = {"password": "new_" + UPDATE_USER_PASSWORD}
    response = await client.put(
        UPDATE_URL,
        json=new_pass_payload,
        headers={
            "Authorization": f"Bearer {generate_access_token(UPDATE_USER_ID)}"
        },
    )

    assert response.status_code == status.HTTP_200_OK

    resq = await session.execute(select(User).where(User.id == UPDATE_USER_ID))
    user = resq.scalar()
    assert user.verify_password(new_pass_payload["password"])


async def test_other_fields_untouched(client, session):
    payload = {"username": "new_" + UPDATE_USER_USERNAME}
    await client.put(
        UPDATE_URL,
        json=payload,
        headers={
            "Authorization": f"Bearer {generate_access_token(UPDATE_USER_ID)}"
        },
    )
    resq = await session.execute(select(User).where(User.id == UPDATE_USER_ID))
    user = resq.scalar()

    assert user.email == UPDATE_USER_EMAIL
    assert user.verify_password(UPDATE_USER_PASSWORD)
