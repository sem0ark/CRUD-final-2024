from datetime import datetime

from pydantic import BaseModel


class BaseTimestamp(BaseModel):
    created_at: datetime
    updated_at: datetime
