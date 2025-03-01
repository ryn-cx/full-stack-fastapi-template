import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.users.models import User


# Reusable properties of the Item model. This will allow schemas to easily inherit the
# properties of the model. This extra class is required because you cannot directly
# inherit types from a SQLModel class.
class ItemType:
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )


# Database model, database table inferred from class name
class Item(ItemType, SQLModel, table=True):
    # The original version of the template allowed None values for the owner field.
    owner: "User" = Relationship(back_populates="items")
