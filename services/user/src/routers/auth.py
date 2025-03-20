from database.models import User

from fastapi import APIRouter, HTTPException, Response, status

import sqlalchemy.exc
from sqlalchemy.sql import select

import src.dependencies as dp
import src.pydmodels as pdm
from src.auth import decode_jwt_token, generate_token_pair


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
async def signup(
    item: pdm.SignUpModel, session: dp.SessionDep, response: Response
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
    form_data: dp.LoginFormData,
    session: dp.SessionDep,
    token_manager: dp.TokenManagerDep,
    response: Response,
):

    query_resp = await session.execute(
        select(User).where(User.username == form_data.username)
    )
    user = query_resp.scalar()

    if user is None or not user.verify_password(form_data.password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "invalid credentials"}

    tokens = generate_token_pair(user.id)

    await token_manager.set_refresh(user.id, tokens["refresh_token"])

    return tokens


@router.post("/refresh")
async def refresh(token: pdm.RefreshToken, token_manager: dp.TokenManagerDep):
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    refresh_token = token.refresh_token
    user_id = decode_jwt_token(refresh_token)

    if user_id is None:
        raise token_exception
    stored_refresh = await token_manager.get_refresh(user_id)

    if stored_refresh is None or stored_refresh != refresh_token:
        raise token_exception

    tokens = generate_token_pair(user_id)
    await token_manager.set_refresh(user_id, tokens["refresh_token"])
    return tokens
