from pydantic import BaseModel
from typing import Optional


class LimitOffsetPaginationParamDTO(BaseModel):
    limit: Optional[int] = 5
    offset: Optional[int] = 0
