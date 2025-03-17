from typing import Annotated

from database.engine import engine

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with sessionmaker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
