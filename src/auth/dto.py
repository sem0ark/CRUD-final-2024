from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str
    # used ID compared to login to later query premissions association
    #   directly, compared to first finding user
    # failed to use user_id directly, because it requires to have string value
