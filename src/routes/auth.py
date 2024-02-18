from fastapi import APIRouter
from passlib.context import CryptContext

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
