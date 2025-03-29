from typing import List

from database.models import File, Post

from fastapi import APIRouter, Query, Response, status

from sqlalchemy import select

from src import dependencies as dp


post = APIRouter(prefix="/post")


@post.get("/get/{post_id}")
async def get_post(post_id: int, session: dp.SessionDep, response: Response):
    requested_post = await session.get(Post, post_id)
    if requested_post is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "post with given ID not found"}
    files = await session.execute(
        select(File.id).where(File.post_id == requested_post.id)
    )
    data = {
        "id": requested_post.id,
        "title": requested_post.title,
        "author_id": requested_post.author_id,
        "content": requested_post.content,
        "creation_date": requested_post.creation_date,
        "last_edit": requested_post.last_edit,
        "attachments": list(files.scalars()),
    }
    return data


@post.get("/files")
async def get_files(id: List[int] = Query(None, alias="id")):
    id_list = [int(given_id) for given_id in id]
    return {"given_ids": id_list}
