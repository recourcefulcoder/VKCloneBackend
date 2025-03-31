from typing import Annotated, Optional

from database.engine import engine

from fastapi import Depends, HTTPException, Request, status

from httpx import AsyncClient

import settings

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def get_session():
    async with async_sessionmaker(engine)() as session:
        yield session


async def fetch_user_id(request: Request) -> Optional[int]:
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid authorization scheme or invalid token",
    )
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        raise unauthorized_exception
    token = auth_header.split(" ")[1]

    async with AsyncClient() as client:
        response = await client.get(
            settings.USER_INFO_LINK,
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code != status.HTTP_200_OK:
            raise unauthorized_exception

    return int(response.json().get("id"))


SessionDep = Annotated[AsyncSession, Depends(get_session)]
FetchUserId = Annotated[int, Depends(fetch_user_id)]
