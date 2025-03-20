from typing import Annotated

from database.engine import engine

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.auth import TokenManager

sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with sessionmaker() as session:
        yield session


def get_token_manager():
    return TokenManager()


SessionDep = Annotated[AsyncSession, Depends(get_session)]
TokenManagerDep = Annotated[TokenManager, Depends(get_token_manager)]
