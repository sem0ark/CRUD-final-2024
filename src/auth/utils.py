from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

import src.auth.dto as auth_dto
import src.auth.utils as auth_utils
import src.user.models as user_models
from src.shared.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from src.shared.logs import log

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_form")


def verify_password(plain_password, hashed_password):
    log.debug("Verifying the password")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    hashed_password = pwd_context.hash(password)
    log.debug("Hashing the password")
    return hashed_password


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=1)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    log.debug(f"Created new token until {expire}")

    return encoded_jwt


def login_user(user: user_models.User) -> auth_dto.Token:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return auth_dto.Token(access_token=access_token, token_type="bearer")
