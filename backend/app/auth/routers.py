from typing import Any

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.api.sche_base import DataResponse
from app.user.schemas import Token
from app.user.services import UserService
from fastapi import status, HTTPException

from core.utils.security import create_access_token
# Read more: https://fastapi.tiangolo.com/ja/advanced/security/oauth2-scopes/

router = APIRouter()


@router.post("/sign-in", response_model=Token)
def sign_in(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = UserService().authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản hoặc mật khẩu không chính xác! Xin vui lòng thử lại, xin cảm ơn.",
        )
    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )
    return Token(access_token=access_token)
