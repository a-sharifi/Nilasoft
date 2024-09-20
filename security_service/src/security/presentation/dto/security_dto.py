from pydantic import BaseModel


class SecurityDataCreateDto(BaseModel):
    title: str


class SecurityDataUpdateDto(BaseModel):
    title: str


class SecurityDataPartialUpdateDto(BaseModel):
    title: str | None = None
