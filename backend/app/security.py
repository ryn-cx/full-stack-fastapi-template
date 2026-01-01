from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import jwt
from passlib.context import CryptContext

from app.config import settings

if TYPE_CHECKING:
    import uuid
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: uuid.UUID, expires_delta: timedelta) -> str:
    expire = datetime.now(UTC) + expires_delta
    to_encode: dict[str, str | datetime] = {"exp": expire, "sub": str(subject)}
    # reportUnknownMemberType - Error is from the original template.
    return jwt.encode(  # pyright: ignore[reportUnknownMemberType]
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
