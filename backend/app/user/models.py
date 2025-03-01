import uuid
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.item.models import Item


# Reusable properties of the User model. This will allow schemas to easily inherit the
# properties of the model. This extra class is required because you cannot directly
# inherit types from a SQLModel class.
class UserType:
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    hashed_password: str


# Database model, database table inferred from class name
class User(UserType, SQLModel, table=True):
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
