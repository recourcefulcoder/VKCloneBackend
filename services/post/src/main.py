from contextlib import asynccontextmanager

from database.models import Post

from fastapi import FastAPI, Response, status

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


@app.get("/post/{post_id}")
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
