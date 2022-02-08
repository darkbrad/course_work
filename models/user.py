from pydantic import BaseModel, Field, validator
from typing import Optional


class RegistrationModel(BaseModel):
    login: str = Field(min_length=6)
    password: str = Field(min_length=8)

    @validator("login")
    def validate_login(cls, login: str) -> str:
        assert " " not in login, "No spaces allowed in login"
        return login


class BaseUserModel(BaseModel):
    id: str
    login: str


class UserModel(BaseUserModel):
    id: str
    login: str
    bills:int
    balance:int
    image:Optional[str]
    password:str