from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..data import crud, schemas
from .auth import authenticate_user, create_access_token
from .dependencies import get_db

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> schemas.Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/auth", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    db_user = crud.create_user(db, user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_user
