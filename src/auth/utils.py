from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple

from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

import src.auth.dto as auth_dto
import src.auth.utils as auth_utils
import src.user.models as user_models
from src.shared.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from src.shared.logs import log

pwd_context = CryptContext(schemes=["bcrypt"])


def get_authorization_scheme_param(
    authorization_header_value: Optional[str],
) -> Tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


class OAuth2PasswordCustomHeader(OAuth2PasswordBearer):
    def __init__(
        self,
        tokenUrl: str,
        custom_header: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        super().__init__(tokenUrl, scheme_name, scopes, description, auto_error)
        self.custom_header = custom_header

    def __call__(self, request: Request):
        authorization = request.headers.get(self.custom_header)

        if authorization is None:
            authorization = request.headers.get("Authorization")
            log.info("Received auth through 'Authorization', not custom header.")
        else:
            log.debug(
                "Received header '%s' while trying to read '%s'",
                authorization,
                self.custom_header,
            )

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordCustomHeader(
    tokenUrl="login_form", custom_header="X-Auth"
)


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
