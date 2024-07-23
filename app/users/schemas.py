from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, EmailStr


class UserCreateModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str


class UserUpdateModel(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None


class UserResponseModel(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    phone_number: str | None
    created_at: datetime
    updated_at: datetime
