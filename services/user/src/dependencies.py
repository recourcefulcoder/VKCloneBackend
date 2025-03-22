from typing import Annotated

from database.engine import engine
from database.models import User

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.sql import select

from src.auth import TokenManager, decode_jwt_token
from src.pydmodels import UserInfo

sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")


async def get_session():
    async with sessionmaker() as session:
        yield session


def get_token_manager():
    return TokenManager()


SessionDep = Annotated[AsyncSession, Depends(get_session)]
TokenManagerDep = Annotated[TokenManager, Depends(get_token_manager)]
LoginFormData = Annotated[OAuth2PasswordRequestForm, Depends()]


async def fetch_user(
    session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]
):
    user_id = decode_jwt_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    res = await session.execute(select(User).where(User.id == user_id))
    user = res.scalar()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    pydantic_user = UserInfo(
        id=user_id,
        email=user.email,
        username=user.username,
        created_date=user.created_date,
    )
    return pydantic_user


FetchUserDep = Annotated[UserInfo, Depends(fetch_user)]
