from importlib import import_module
from pathlib import Path

from fastapi import APIRouter

from app.config import settings

api_router = APIRouter()


def automatically_load_routers() -> None:
    """Automatically load all of the routers from app/*/router.py"""
    app_folder = Path(__file__).parent

    for model_files in app_folder.glob("*/router.py"):
        module_name = model_files.parent.name
        router = import_module(f"app.{module_name}.router").router

        if module_name == "private":
            if settings.ENVIRONMENT == "local":
                api_router.include_router(router)
        else:
            api_router.include_router(router)


def manually_load_routers() -> None:
    """Manually load all of the routers.

    This function is left as an example of how to manually load routers if they do not
    fit the folder structure supported by automatically_load_routers."""

    # Example of how to import models manually
    # from app.items.router import router as items_router
    # from app.login.router import router as login_router
    # from app.private.router import router as private_router
    # from app.users.router import router as users_router
    # from app.utils.router import router as utils_router

    # api_router = APIRouter()
    # api_router.include_router(login_router)
    # api_router.include_router(users_router)
    # api_router.include_router(utils_router)
    # api_router.include_router(items_router)

    # if settings.ENVIRONMENT == "local":
    #     api_router.include_router(private_router)


if settings.AUTOMATICALLY_LOAD_ROUTES:
    automatically_load_routers()
else:
    manually_load_routers()
