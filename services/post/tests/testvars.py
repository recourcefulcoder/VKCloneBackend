import datetime


POST_DATA = {
    "id": 1,
    "author_id": 1,
    "title": "Cute post title UwU",
    "content": '<div style="color:red";>Cute post content</div>',
    "creation_date": datetime.datetime(
        year=2012, month=4, day=13, hour=13, minute=29, second=13
    ),
    "last_edit": None,
}


FILE_DATA = {
    "id": 1,
    "filename": "static/cute_ears.jpg",
}

POST_TO_FILE_BOUNDS = [
    {
        "post_id": 1,
        "file_id": 1,
    }
]

TEST_BASE_URL = "http://test"

GRAPHQL_ENDPOINT_URL = "/post/graphql"
