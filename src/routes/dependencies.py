from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ..config import ALGORITHM, SECRET_KEY
from ..data.crud import get_project_role, get_user
from ..data.database import SessionLocal
from ..data.schemas import TokenData
from ..data.types import PermissionType
from ..utils.logs import getLogger
from .auth import oauth2_scheme

log = getLogger()


def get_db():
    db = SessionLocal()  # a "proxy" of a SQLAlchemy Session
    try:
        yield db
    finally:
        db.close()
    # This way we make sure the database session is always closed after the request.


# placed here due to cyclic dependency on get_db
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
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


# https://stackoverflow.com/questions/68668417/
#   is-it-possible-to-pass-path-arguments-into-fastapi-dependency-functions


def project_role(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project_role = get_project_role(db, project_id, current_user.id)
    if not project_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return project_role


def is_owner(project_role: PermissionType = Depends(project_role)):
    if project_role != PermissionType.owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


# implemented for readability
def is_participant(_project_role: PermissionType = Depends(project_role)):
    return True
