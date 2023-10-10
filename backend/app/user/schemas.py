from enum import Enum
from typing import Optional
from datetime import datetime

from email_validator import EmailNotValidError
from pydantic import BaseModel, EmailStr, field_validator, validate_email


class UserRole(Enum):
    ADMIN = 'admin'
    GUEST = 'guest'


# Read more here:
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-initial-pydantic-models-schemas

# Shared properties
class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True

    @classmethod
    @field_validator('email')
    def val_email(cls, email: EmailStr) -> EmailStr:
        try:
            validate_email(email)
        except EmailNotValidError:
            raise ValueError("Invalid email format")
        return email


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
    username: Optional[str] = None
