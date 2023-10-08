import enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserRole(enum.Enum):
    ADMIN = 'admin'
    GUEST = 'guest'


# Read more here:
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-initial-pydantic-models-schemas

# Shared properties
class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class UserItemResponse(UserBase):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    role: str
    last_login: Optional[datetime]


class UserCreateRequest(UserBase):
    full_name: Optional[str]
    password: str
    email: EmailStr
    is_active: bool = True
    role: UserRole = UserRole.GUEST


class UserRegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.GUEST


class UserUpdateMeRequest(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class UserUpdateRequest(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool] = True
    role: Optional[UserRole]


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenPayload(BaseModel):
    user_id: Optional[int] = None
