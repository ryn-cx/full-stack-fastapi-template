from importlib import import_module
from pathlib import Path

from sqlmodel import Session, create_engine, select

from app.config import settings
from app.users import service
from app.users.models import User
from app.users.schemas import UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    load_models()

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER),
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = service.create_user(session=session, user_create=user_in)


def load_models() -> None:
    """Automatically load all of the models from app/*/models.py."""
    app_folder = Path(__file__).parent

    for model_file in app_folder.glob("*/models.py"):
        import_module(f"app.{model_file.parent.name}.models")
