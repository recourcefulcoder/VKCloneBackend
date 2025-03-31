import io
from http import HTTPStatus

from httpx import Response

import pytest

import pytest_asyncio

from src.main import app


pytestmark = pytest.mark.asyncio

ENDPOINT_LINK = app.url_path_for("create_post")


@pytest_asyncio.fixture
async def token():
    return "valid_token"


async def test_401_on_missing_token(client):
    response = await client.post(
        ENDPOINT_LINK,
        data={
            "title": "new_title",
            "content": "<h1>Test content!</h1>",
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_401_on_invalid_token(client, mocker):
    mocker.patch(
        "httpx.AsyncClient.get",
        return_value=Response(
            status_code=401,
            json={"detail": "Invalid authentication credentials"},
        ),
    )
    response = await client.post(
        ENDPOINT_LINK,
        data={
            "title": "new_title",
            "content": "<h1>Test content!</h1>",
        },
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_200_on_valid_request(client, mocker):
    mocker.patch(
        "httpx.AsyncClient.get",
        return_value=Response(status_code=200, json={"id": 1}),
    )

    fake_file = io.BytesIO(b"fake file content")
    files = {"file": ("test.txt", fake_file, "text/plain")}
    data = {
        "title": "new_title",
        "content": "<h1>Test content!</h1>",
    }

    response = await client.post(
        ENDPOINT_LINK,
        data=data,
        files=files,
        headers={"Authorization": "Bearer any_token"},
    )
    assert response.status_code == HTTPStatus.OK


async def test_200_on_valid_request_without_file(client, mocker):
    mocker.patch(
        "httpx.AsyncClient.get",
        return_value=Response(status_code=200, json={"id": 1}),
    )

    response = await client.post(
        ENDPOINT_LINK,
        data={
            "title": "new_title",
            "content": "<h1>Test content!</h1>",
        },
        headers={"Authorization": "Bearer any_token"},
    )
    assert response.status_code == HTTPStatus.OK


async def test_400_on_invalid_form_data(client):
    pass


async def test_400_on_json_request(client):
    pass


async def test_valid_file_saving(client):
    """Ensures that files sent to backend are saved
    and are saved in proper format, as described in documentation"""
    pass


async def test_valid_post_data_saved_in_database(client):
    pass


async def test_valid_files_data_saved_in_database(client):
    pass


@pytest.mark.parametrize(
    "method",
    [
        "GET",
        "PUT",
        "PATCH",
        "DELETE",
    ],
)
async def test_only_post_allowed(method, client):
    response = await client.request(method, ENDPOINT_LINK)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
