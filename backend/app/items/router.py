import uuid  # noqa: TC003

from fastapi import APIRouter, HTTPException, status
from sqlmodel import func, select

from app.dependencies import SessionDep  # noqa: TC001
from app.items.models import Item
from app.items.schemas import ItemCreate, ItemPublic, ItemsPublic, ItemUpdate
from app.schemas import Message
from app.users.dependencies import CurrentUser  # noqa: TC001

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
def read_items(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> ItemsPublic:
    """
    Retrieve items.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Item)
        count = session.exec(count_statement).one()
        statement = select(Item).offset(skip).limit(limit)
        items = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Item)
            .where(Item.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Item)
            .where(Item.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        items = session.exec(statement).all()

    return ItemsPublic(
        data=[ItemPublic.model_validate(item) for item in items],
        count=count,
    )


@router.get("/{id}", response_model=ItemPublic)
def read_item(
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,  # noqa: A002 - This is the name given by the original template.
) -> Item:
    """
    Get item by ID.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return item


@router.post("/", response_model=ItemPublic)
def create_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    item_in: ItemCreate,
) -> Item:
    """
    Create new item.
    """
    item = Item.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put("/{id}", response_model=ItemPublic)
def update_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,  # noqa: A002 - This is the name given by the original template.
    item_in: ItemUpdate,
) -> Item:
    """
    Update an item.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    update_dict = item_in.model_dump(exclude_unset=True)
    item.sqlmodel_update(update_dict)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{id}")
def delete_item(
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,  # noqa: A002 - This is the name given by the original template.
) -> Message:
    """
    Delete an item.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    session.delete(item)
    session.commit()
    return Message(message="Item deleted successfully")
