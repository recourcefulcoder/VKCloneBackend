from datetime import timedelta

from fastapi import status

import pytest

from src.auth import generate_access_token, generate_jwt_token
from src.main import app

from . import pytestmark, testvars


USER_ID = testvars.USER_IDS[0]
INFO_LINK = app.url_path_for("get_personal_info")


async def test_200_on_valid_token(client):
    response = await client.get(
        INFO_LINK,
        headers={"Authorization": f"Bearer {generate_access_token(USER_ID)}"},
    )
    assert response.status_code == status.HTTP_200_OK


async def test_valid_payload_returned(client):
    response = await client.get(
        INFO_LINK,
        headers={"Authorization": f"Bearer {generate_access_token(USER_ID)}"},
    )
    keys = response.json().keys()
    assert "id" in keys
    assert "username" in keys
    assert "email" in keys
    assert "created_date" in keys


@pytest.mark.parametrize(
    "token",
    [
        "invalid",
        "",
        generate_access_token(testvars.USERS_AMOUNT + 1),  # not existing user
        generate_jwt_token(USER_ID, timedelta(minutes=-1)),
    ],
)
async def test_401_on_invalid_token(token, client):
    response = await client.get(
        INFO_LINK, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_401_on_missing_token(client):
    response = await client.get(
        INFO_LINK,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
