from datetime import datetime
from typing import Optional

from app.schemas.user_role import UserRole
from pydantic import UUID4, BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    account_id: Optional[UUID4] = None


class UserCreate(UserBase):
    password: str
    account_id: UUID4


class UserUpdate(BaseModel):
    full_name: str
    phone_number: str
    email: EmailStr


class UserInDBBase(UserBase):
    id: UUID4
    user_role: Optional[UserRole]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserRegister(BaseModel):
    password: str
    email: EmailStr
    full_name: str
    phone_number: str


class UserInDB(UserInDBBase):
    hashed_password: str
