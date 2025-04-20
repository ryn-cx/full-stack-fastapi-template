from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.core.db import init_db
from app.dependencies import get_db
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def test_engine() -> Generator[Engine, None, None]:
    test_engine = create_engine(str(settings.SQLALCHEMY_TEST_DATABASE_URI))
    SQLModel.metadata.drop_all(bind=test_engine)
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    SQLModel.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def db(test_engine: Engine) -> Generator[Session, None, None]:
    with Session(test_engine) as session:
        init_db(session)
        yield session


@pytest.fixture(scope="module")
def client(db: Session) -> Generator[TestClient, None, None]:
    def get_db_override() -> Session:
        return db

    app.dependency_overrides[get_db] = get_db_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
