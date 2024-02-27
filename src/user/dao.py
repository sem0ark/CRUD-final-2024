from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.user.dto import UserDB
from src.user.models import User


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).get(user_id)


def get_user_by_login(db: Session, login: str) -> User | None:
    return db.query(User).filter(User.login == login).first()


def create_user(db: Session, user: UserDB) -> User | None:
    db_user = User(login=user.login, hashed_password=user.hashed_password)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None

    db.refresh(db_user)
    return db_user
