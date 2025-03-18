import subprocess
from contextlib import asynccontextmanager

import config

from fastapi import FastAPI

from .routers import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    proc = None
    if config.DEBUG:
        proc = subprocess.Popen("redis-server --port 6379", shell=True)
    yield
    if config.DEBUG:
        proc.kill()


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}
