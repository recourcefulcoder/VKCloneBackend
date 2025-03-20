from typing import Annotated

from fastapi import APIRouter, Depends

import src.dependencies as dp

from .auth import router as auth_router

router = APIRouter(prefix="/user", tags=["user"])
router.include_router(auth_router)


@router.get("/info")
async def get_personal_info(user: dp.FetchUserDep):
    return user.model_dump()


@router.get("/items")
async def get_items(token: Annotated[str, Depends(dp.oauth2_scheme)]):
    return {"token": token}
