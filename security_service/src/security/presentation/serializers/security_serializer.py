from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SecurityDataSerializer(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

