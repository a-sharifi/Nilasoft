from pydantic import BaseModel
from typing import List


class UserSerializer(BaseModel):
    id: str
    name: str
    family: str
    email: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class AuthPayload(BaseModel):
    sub: str
    iat: int
    exp: int
    permissions: List[str]
    scope: str | None = None

    class Config:
        from_attributes = True


class TokenResponseSerializer(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

    class Config:
        from_attributes = True
