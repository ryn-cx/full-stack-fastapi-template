from importlib import import_module
from pathlib import Path

from sqlmodel import Session, create_engine, select

from app import crud
from app.config import settings
from app.users.models import User
from app.users.schemas import UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)


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
    # from app.users.models import User
    # from app.items.models import Item


def load_models() -> None:
    if settings.AUTOMATICALLY_LOAD_MODELS:
        automatically_load_models()
    else:
        manually_load_models()
