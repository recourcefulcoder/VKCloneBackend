from fastapi import status

import pytest

from . import testvars


GET_FUNCTION_NAME = "get_post"


def form_query_string(requested_fields):
    return f"post \u007b {' '.join(requested_fields)} \u007d"


@pytest.mark.asyncio
async def test_200_on_valid_query(client):
    payload = {"query": "query { post { id } }"}
    response = await client.post(
        testvars.GRAPHQL_ENDPOINT_URL,
        json=payload,
    )
    assert response.status_code == status.HTTP_200_OK


# @pytest.mark.parametrize(
#     "requested_fields",
#     [
#         ["id", "title"],
#         ["id", "title"],
#         ["id", "title"],
#     ]
# )
# @pytest.mark.asyncio
# async def test_valid_payload_on_valid_id(client, requested_fields):
#     response = await client.post(
#         testvars.GRAPHQL_ENDPOINT_URL,
#         json={
#             "query": form_query_string(requested_fields),
#         },
#     )
#     keys = response.json().keys()
#     assert response.status_code == status.HTTP_200_OK
#     assert all(elem in keys for elem in requested_fields)
#     assert len(requested_fields) == len(keys)
