from database.models import User

from fastapi import APIRouter, Response, status

import sqlalchemy.exc

import src.dependencies as dp
from src.pydmodels import SignUpModel


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/signup")
async def signup(
    item: SignUpModel, session: dp.SessionDep, response: Response
):
    user = User(**item.model_dump())
    session.add(user)
    try:
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT
        return {"error": "user with given email/username already exists"}
    return item.model_dump()
