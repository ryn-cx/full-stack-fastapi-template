from sqlmodel import Session

from app.security import verify_password
from app.users.models import User
from app.users.service import get_user_by_email


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
