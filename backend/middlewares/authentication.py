from typing import Optional, Tuple
from jose import jwt
from pydantic import ValidationError
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection
from core.config import settings
import models
import schemas


class AuthBackend(AuthenticationBackend):
    async def authenticate(
            self,
            conn: HTTPConnection
    ) -> Tuple[bool, Optional[models.User]]:
        current_user = models.User()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, credentials = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not credentials:
            return False, current_user

        try:
            payload = jwt.decode(
                credentials, settings.secret_key, algorithms=[settings.jwt_algorithm]
            )
            token_data = schemas.TokenPayload(**payload)
        except (jwt.JWTError, ValidationError):
            return False, current_user
        current_user.id = token_data.sub
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
