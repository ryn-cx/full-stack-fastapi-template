import uuid  # noqa: TC003 - Required for SQLModel

from sqlmodel import Field, SQLModel

from app.items.models import ItemBase


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    # assignment - This is just how the item schema was designed in the original
    # template.
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore[assignment]


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int
