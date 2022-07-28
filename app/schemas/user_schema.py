from datetime import datetime

from pydantic import BaseModel, EmailStr, validator, PositiveInt

from app.utils.auth_utils import hash_password
from app.database.models import UserStatus


class UserBase(BaseModel):
    email: EmailStr


class UserRegister(UserBase):
    password1: str
    password2: str

    @property
    def hashed_password(self):
        return hash_password(self.password1)

    @validator("password2")
    def password_match(cls, v, values):
        if v != values.get('password1'):
            raise ValueError("passwords does not match")
        return v


class User(UserBase):
    id: PositiveInt
    status: UserStatus
    datetime_of_created: datetime
    datetime_of_updated: datetime

    class Config:
        orm_mode = True
