import datetime


POST_ID = 1

POST_DATA = {
    "id": POST_ID,
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
    "post_id": POST_ID,
    "filename": "static/cute_ears.jpg",
}

TEST_BASE_URL = "http://test"

GRAPHQL_ENDPOINT_URL = "/post/graphql"
