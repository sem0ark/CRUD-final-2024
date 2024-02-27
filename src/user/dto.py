from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    login: str = Field(max_length=200)


class UserCreate(UserBase):
    password: str = Field(
        min_length=6, description="Password should be at least 6 characters long"
    )


class UserDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str
    # used ID compared to login to later query premissions association
    #   directly, compared to first finding user
    # failed to use user_id directly, because it requires to have string value
