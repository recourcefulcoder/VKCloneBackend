from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routers.post import post


@asynccontextmanager
async def lifespan(app: FastAPI):
    processes = []
    # if settings.DEBUG:
    #     processes.append(subprocess.Popen("", shell=True))
    yield
    for proc in processes:
        proc.kill()


app = FastAPI(lifespan=lifespan)
app.include_router(post)
