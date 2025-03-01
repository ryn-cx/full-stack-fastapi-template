from fastapi import APIRouter

from app.api.routes import login, private, utils
from app.core.config import settings
from app.item import router
from app.user import users

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(router.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
