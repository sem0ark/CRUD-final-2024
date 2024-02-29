from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from src.shared.config import ALGORITHM, SECRET_KEY
from src.shared.logs import log

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_form")


def verify_password(plain_password, hashed_password):
    log.debug(
        f"Trying to verify password '{plain_password}' with hash '{hashed_password}'"
    )
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    hashed_password = pwd_context.hash(password)
    log.debug(f"Trying to hash password '{password}' into hash '{hashed_password}'")
    return hashed_password


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=5)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt