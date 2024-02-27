from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.auth.auth import oauth2_scheme
from src.shared.config import ALGORITHM, SECRET_KEY
from src.shared.database import get_db
from src.shared.logs import log
from src.user.dao import get_user
from src.user.dao import get_user_by_login as get_by_login
from src.user.dto import TokenData
from src.user.models import User


def get_user_by_login(login: str, db: Session = Depends(get_db)) -> User:
    db_user = get_by_login(db, login)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        log.debug(f"Trying to process token '{token}'")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        log.debug(f"Received payload '{payload}' from the token")

        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id)
    except JWTError as e:
        log.debug(e)
        raise credentials_exception from None
        # B904 raise exceptions with `raise ... from None`
        # to distinguish them from errors in exception handlin

    user = get_user(
        db, int(token_data.user_id)
    )  # because bcrypt requires string subject
    if user is None:
        raise credentials_exception

    return user
