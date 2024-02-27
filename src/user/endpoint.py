from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth.auth import authenticate_user, create_access_token, get_password_hash
from src.data import crud, models, schemas
from src.routes.dependencies import get_db
from src.shared.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


def login_user(user: models.User | None) -> schemas.Token:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/login_form")
async def login_for_access_token_form(
    sign_in: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> schemas.Token:
    user = authenticate_user(db, sign_in.username, sign_in.password)
    return login_user(user)


@router.post("/login")
async def login_for_access_token(
    sign_in: schemas.UserCreate,
    db: Session = Depends(get_db),
) -> schemas.Token:
    user = authenticate_user(db, sign_in.login, sign_in.password)
    return login_user(user)


@router.post("/auth", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    db_user = crud.create_user(
        db,
        schemas.UserDB(
            login=user.login, hashed_password=get_password_hash(user.password)
        ),
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_user
