from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    name: str
    family: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UserLoginDTO(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
