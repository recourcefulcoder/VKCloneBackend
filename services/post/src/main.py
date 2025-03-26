from contextlib import asynccontextmanager
from typing import List

from database.models import Post

from fastapi import FastAPI,  Query, Response, status

from . import dependencies as dp
from . import pydmodels as pym


@asynccontextmanager
async def lifespan(app: FastAPI):
    processes = []
    # if settings.DEBUG:
    #     processes.append(subprocess.Popen("", shell=True))
    yield
    for proc in processes:
        proc.kill()


app = FastAPI(lifespan=lifespan)


@app.get("/post/get/{post_id}")
async def get_post(post_id: int, session: dp.SessionDep, response: Response):
    post = await session.get(Post, post_id)
    if post is None:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"error": "post with given ID not found"}
    post = pym.PostInfo(
        id=post.id,
        title=post.title,
        author_username=post.author_username,
        content=post.content,
        creation=post.creation_date,
    )
    return post.model_dump()


@app.get("/post/files")
async def get_files(id: List[int] = Query(None, alias="id")):
    id_list = [int(given_id) for given_id in id]
    return {"given_ids": id_list}
