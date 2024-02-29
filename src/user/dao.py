from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import src.user.dto as user_dto
import src.user.models as user_models


def get_user(db: Session, user_id: int) -> user_models.User | None:
    return db.query(user_models.User).get(user_id)


def get_user_by_login(db: Session, login: str) -> user_models.User | None:
    return db.query(user_models.User).filter(user_models.User.login == login).first()


def create_user(db: Session, user: user_dto.UserDB) -> user_models.User | None:
    db_user = user_models.User(login=user.login, hashed_password=user.hashed_password)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None

    db.refresh(db_user)
    return db_user
