from typing import TYPE_CHECKING

from app.items import service
from app.items.schemas import ItemCreate
from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string

if TYPE_CHECKING:
    from sqlmodel import Session

    from app.items.models import Item


def create_random_item(db: Session) -> Item:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    return service.create_item(session=db, item_in=item_in, owner_id=owner_id)
