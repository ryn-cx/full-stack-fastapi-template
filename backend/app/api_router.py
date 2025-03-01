from fastapi import APIRouter

from app.api.routes import utils
from app.core.config import settings
from app.items import router
from app.login import routes
from app.users import users

api_router = APIRouter()
api_router.include_router(routes.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(router.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(routes.router)
