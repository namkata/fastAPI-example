from fastapi import APIRouter
from app.user import routers as user_routers
from app.auth import routers as auth_routers

api_router = APIRouter()

api_router.include_router(user_routers.router, tags=["user"], prefix="/users")
api_router.include_router(auth_routers.router, tags=["auth"], prefix="/auth")
