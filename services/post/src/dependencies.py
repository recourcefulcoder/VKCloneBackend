from typing import Annotated

from database.engine import engine

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def get_session():
    async with async_sessionmaker(engine)() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
