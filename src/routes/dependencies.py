from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ..config import ALGORITHM, SECRET_KEY
from ..data import crud, models
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
) -> models.User:
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

    user = crud.get_user(
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
) -> models.Permission:
    project_role = crud.get_project_role(db, project_id, current_user.id)
    if not project_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have access to the project",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return project_role


def is_project_owner(project_role: models.Permission = Depends(project_role)) -> bool:
    if project_role.permission != PermissionType.owner.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the project owner",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


# implemented for readability
def is_project_participant(
    _project_role: PermissionType = Depends(project_role),
) -> bool:
    return True


def get_project_by_id(project_id: int, db: Session = Depends(get_db)) -> models.Project:
    db_project = crud.get_project(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return db_project


def get_user_by_login(login: str, db: Session = Depends(get_db)) -> models.User:
    db_user = crud.get_user_by_login(db, login)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user
