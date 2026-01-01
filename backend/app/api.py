from importlib import import_module
from pathlib import Path

from fastapi import APIRouter

from app.config import settings

api_router = APIRouter()

# Automatically load all of the routers from app/*/router.py and add them to the
# api_router.
app_folder = Path(__file__).parent
for model_files in app_folder.glob("*/router.py"):
    module_name = model_files.parent.name
    router = import_module(f"app.{module_name}.router").router

    if module_name == "private":
        if settings.ENVIRONMENT == "local":
            api_router.include_router(router)
    else:
        api_router.include_router(router)
