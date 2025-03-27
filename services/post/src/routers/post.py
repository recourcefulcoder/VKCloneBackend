from typing import List

from database.models import Post

from fastapi import APIRouter, Query, Response, status

from src import dependencies as dp, pydmodels as pym
from src.routers.graphql import graphql_app


post = APIRouter(prefix="/post")
post.include_router(graphql_app, prefix="/graphql")


@post.get("/get/{post_id}")
async def get_post(post_id: int, session: dp.SessionDep, response: Response):
    returned_post = await session.get(Post, post_id)
    if returned_post is None:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"error": "post with given ID not found"}
    pydantic_post = pym.PostInfo(
        id=returned_post.id,
        title=returned_post.title,
        author_id=returned_post.author_id,
        content=returned_post.content,
        creation=returned_post.creation_date,
    )
    return pydantic_post.model_dump()


@post.get("/files")
async def get_files(id: List[int] = Query(None, alias="id")):
    id_list = [int(given_id) for given_id in id]
    return {"given_ids": id_list}
