from fastapi import APIRouter

from .auth import router as auth_router

router = APIRouter(prefix="/user", tags=["user"])
router.include_router(auth_router)
