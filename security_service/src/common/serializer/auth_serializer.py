from typing import List

from pydantic import BaseModel


class AuthPayload(BaseModel):
    sub: int
    iat: int
    exp: int
    permissions: List[str]
    scope: str | None = None

    class Config:
        from_attributes = True