from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import src.auth.dao as auth_dao
import src.auth.dto as auth_dto
import src.auth.utils as auth_utils
import src.user.dao as user_dao
import src.user.dto as user_dto
from src.shared.database import get_db

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login_form")
async def login_for_access_token_form(
    sign_in: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> auth_dto.Token:
    user = auth_dao.authenticate_user(db, sign_in.username, sign_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return auth_utils.login_user(user)


@router.post("/login")
async def login_for_access_token(
    sign_in: user_dto.UserCreate,
    db: Session = Depends(get_db),
) -> auth_dto.Token:
    user = auth_dao.authenticate_user(db, sign_in.login, sign_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return auth_utils.login_user(user)


@router.post("/auth", response_model=user_dto.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: user_dto.UserCreate, db: Session = Depends(get_db)
) -> user_dto.User:
    db_user = user_dao.create_user(
        db,
        user_dto.UserDB(
            login=user.login,
            hashed_password=auth_utils.get_password_hash(user.password),
        ),
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_user
