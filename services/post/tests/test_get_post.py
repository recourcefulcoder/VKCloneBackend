from fastapi import status

import pytest

from src.main import app

from . import testvars

pytestmark = pytest.mark.asyncio


ENDPOINT_LINK = app.url_path_for(
    "get_post", post_id=testvars.POST_DATA.get("id")
)


async def test_200_on_valid_request(client):
    response = await client.get(ENDPOINT_LINK)
    assert response.status_code == 200


async def test_404_on_invalid_id(client):
    response = await client.get(app.url_path_for("get_post", post_id=5))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "method",
    [
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
    ],
)
async def test_only_get_allowed(method, client):
    response = await client.request(method, ENDPOINT_LINK)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


async def test_response_json_format(client):
    required_response_keys = [
        "id",
        "title",
        "author_id",
        "content",
        "creation_date",
        "last_edit",
        "attachments",
    ]

    response = await client.get(ENDPOINT_LINK)

    data_keys = response.json().keys()
    assert all(field in data_keys for field in required_response_keys)
    assert len(required_response_keys) == len(data_keys)


async def test_valid_attachments(client):
    response = await client.get(ENDPOINT_LINK)
    data = response.json()
    assert type(data["attachments"]) is list
    assert testvars.FILE_DATA.get("id") in data["attachments"]
    assert len(data["attachments"]) == 1
