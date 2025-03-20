from typing import Annotated

from database.models import User

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.sql import select

import src.dependencies as dp
from src.auth import decode_access_token

from .auth import router as auth_router

router = APIRouter(prefix="/user", tags=["user"])
router.include_router(auth_router)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")


@router.get("/info")
async def get_personal_info(
    session: dp.SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    sub = decode_access_token(token)
    if sub is None:
        raise credentials_exception
    res = await session.execute(select(User).where(User.email == sub))
    user = res.scalar()
    if user is None:
        raise credentials_exception
