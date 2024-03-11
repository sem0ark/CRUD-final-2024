from sqlalchemy.orm import Session

import src.auth.utils as auth_utils
import src.user.dao as user_dao
from src.shared.logs import log


def authenticate_user(db: Session, login: str, password: str):
    user = user_dao.get_user_by_login(db, login)
    log.debug(f"Authenticating user {login}")
    if not user:
        log.info(f"Was not able to find user {login}")
        return False
    if not auth_utils.verify_password(password, user.hashed_password):
        log.info(f"Password verification for {login} failed")
        return False
    log.debug("Authentication successed")
    return user
