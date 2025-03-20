import secrets

import config

from database.models import User

from fastapi import APIRouter, Response, status

import sqlalchemy.exc
from sqlalchemy.sql import select

import src.dependencies as dp
from src.auth import generate_access_token
from src.pydmodels import LoginModel, SignUpModel

router = APIRouter(prefix="/auth", tags=["auth"])


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


@router.post("/login")
async def login(
    item: LoginModel,
    session: dp.SessionDep,
    token_manager: dp.TokenManagerDep,
    response: Response,
):

    if item.username is not None:
        query_resp = await session.execute(
            select(User).where(User.username == item.username)
        )
    else:
        query_resp = await session.execute(
            select(User).where(User.email == item.email)
        )
    user = query_resp.scalar()

    if user is None or not user.verify_password(item.password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "invalid credentials"}

    tokens = {
        "refresh_token": secrets.token_urlsafe(32),
        "access_token": generate_access_token(user.email),
    }

    await token_manager.setex(
        tokens["refresh_token"], config.REFRESH_EXP_TIME, user.email
    )

    return tokens
