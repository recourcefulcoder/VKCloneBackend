import subprocess
from contextlib import asynccontextmanager

import config

from database.event_listeners import initialize_orm_listeners

from fastapi import FastAPI

from .routers import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    proc = []
    if config.DEBUG:
        proc.append(subprocess.Popen("redis-server --port 6379", shell=True))
        proc.append(
            subprocess.Popen(
                "celery -A celery_app worker --detach --loglevel=info",
                shell=True,
            )
        )
    initialize_orm_listeners()
    yield
    for pr in proc:
        pr.kill()


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}
