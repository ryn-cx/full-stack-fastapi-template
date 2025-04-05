from fastapi import APIRouter

from app.core.config import settings
from app.items.router import router as items_router
from app.login.router import router as login_router
from app.private.router import router as private_router
from app.users.router import router as users_router
from app.utils.router import router as utils_router

api_router = APIRouter()
api_router.include_router(items_router)
api_router.include_router(login_router)
api_router.include_router(users_router)
api_router.include_router(utils_router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private_router)
