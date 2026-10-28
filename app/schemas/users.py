import uuid

from app.schemas.base import BasePydanticModel
from pydantic import EmailStr, ConfigDict

class UserBase(BasePydanticModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
