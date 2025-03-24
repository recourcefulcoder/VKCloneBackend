from database.models import User

from fastapi import APIRouter

from sqlalchemy.sql import update

import src.dependencies as dp
import src.pydmodels as pdm

from .auth import router as auth_router

router = APIRouter(prefix="/user", tags=["user"])
router.include_router(auth_router)


@router.get("/info")
async def get_personal_info(user: dp.FetchUserDep):
    return user.model_dump()


@router.put("/change-info")
async def update_user(
    user: dp.FetchUserDep,
    payload: pdm.UserUpdate,
    session: dp.SessionDep,
):

    update_vals = dict()
    for key, value in payload.model_dump().items():
        if value is not None:
            update_vals[key] = value

    if "password" in update_vals.keys():
        update_vals["_password"] = User.hash_password(update_vals["password"])
        del update_vals["password"]

    if bool(update_vals):
        await session.execute(
            update(User).where(User.id == user.id).values(**update_vals)
        )
        await session.commit()
        for key, value in update_vals.items():
            setattr(user, key, value)

    return user.model_dump()
