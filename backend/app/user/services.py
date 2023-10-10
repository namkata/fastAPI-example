# Read more here: https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils
from jose import JWTError, jwt

from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_sqlalchemy import db
from pydantic import ValidationError
from starlette import status

from app.api.sche_base import DataResponse
from app.user.models import User
from settings.config import settings
from core.utils.common import verify_password, get_password_hash
from app.user.schemas import (
    UserCreateRequest, UserUpdateMeRequest, UserUpdateRequest,
    UserRegisterRequest, TokenPayload)


class UserService(object):
    __instance = None

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_str}/auth/sign-in")

    @staticmethod
    def authenticate(*, email: str, password: str) -> Optional[User]:
        """
        Check username and password is correct.
        Return object User if correct, else return None
        """
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
        """
        Decode JWT token to get user_id => return User info from DB query
        """
        try:
            payload = jwt.decode(
                token, settings.secret_key,
                algorithms=[settings.jwt_algorithm]
            )

            username: str = payload.get("sub")
        except(JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Mã bảo mật có thể không đúng, hệ thống không thể xử lý lúc này, vui lòng thử lại sau!",
            )
        user = db.session.query(User).filter_by(email=username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không thể tìm thấy mã bảo mật này cho bất kì "
                       "người dùng nào, chúng tôi sẽ thông báo bạn sau, xin cảm ơn!",
            )
        return user

    @staticmethod
    def register_user(data: UserRegisterRequest):
        register_user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=True,
            role=data.role.value,
        )
        db.session.add(register_user)
        db.session.commit()
        return register_user

    @staticmethod
    def create_user(data: UserCreateRequest):
        new_user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=data.is_active,
            role=data.role.value,
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_me(data: UserUpdateMeRequest, current_user: User):
        current_user.full_name = current_user.full_name if data.full_name is None else data.full_name
        current_user.email = current_user.email if data.email is None else data.email
        current_user.hashed_password = current_user.hashed_password if data.password is None else get_password_hash(
            data.password)
        db.session.commit()
        return current_user

    @staticmethod
    def update(user: User, data: UserUpdateRequest):
        user.full_name = user.full_name if data.full_name is None else data.full_name
        user.email = user.email if data.email is None else data.email
        user.hashed_password = user.hashed_password if data.password is None else get_password_hash(
            data.password)
        user.is_active = user.is_active if data.is_active is None else data.is_active
        user.role = user.role if data.role is None else data.role.value
        db.session.commit()
        return user
