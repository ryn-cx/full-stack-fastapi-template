from importlib import import_module
from pathlib import Path

from sqlmodel import SQLModel


def automatically_load_models() -> None:
    """Automatically load all of the models from app/*/models.py"""
    app_folder = Path(__file__).parent

    for model_files in app_folder.glob("*/models.py"):
        module_name = model_files.parent.name
        import_module(f"app.{module_name}.models")


def manually_load_models() -> None:
    """Manually load all of the models.

    This function is left as an example of how to manually load models if they do not
    fit the folder structure supported by automatically_load_models."""

    # Example of how to import models manually
    # from app.items.models import Item
    # from app.users.models import User


automatically_load_models()
target_metadata = SQLModel.metadata
