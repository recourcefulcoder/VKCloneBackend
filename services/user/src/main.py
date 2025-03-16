from typing import Annotated

from database.engine import engine
from database.models import User

from fastapi import Depends, FastAPI, Response, status

from pydmodels import SignUpModel

import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

app = FastAPI()

sessionmaker = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def get_session():
    async with sessionmaker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


@app.post("/signup")
async def signup(item: SignUpModel, session: SessionDep, response: Response):
    try:
        user = User(**item.dict())
    except ValueError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": f"{e}"}
    user.set_password(item.password)
    session.add(user)
    try:
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT
        return {"error": "user with given email/username already exists"}
    return item.dict()
