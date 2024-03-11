from datetime import datetime
from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


class BaseTimestamp(BaseModel):
    created_at: datetime
    updated_at: datetime


M = TypeVar("M")


class PaginatedResponse(GenericModel, Generic[M]):
    count: int = Field(description="Number of items returned in the response")
    items: List[M] = Field(
        description="List of items returned in the response following given criteria"
    )
