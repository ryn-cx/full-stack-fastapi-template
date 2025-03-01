from fastapi import APIRouter

from app.core.config import settings
from app.items.router import router as items
from app.login.router import router as login
from app.private.router import router as private
from app.router import router as utils
from app.users.router import router as users

api_router = APIRouter()
api_router.include_router(login)
api_router.include_router(users)
api_router.include_router(utils)
api_router.include_router(items)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private)
