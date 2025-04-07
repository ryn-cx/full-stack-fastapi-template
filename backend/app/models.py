from importlib import import_module
from pathlib import Path

from sqlmodel import MetaData, SQLModel


def automatically_load_models() -> MetaData:
    """Automatically load all of the models from app/*/models.py"""
    app_folder = Path(__file__).parent
    for model_file in app_folder.glob("*/models.py"):
        module_name = model_file.parent.name
        import_module(f"app.{module_name}.models")

    return SQLModel.metadata
