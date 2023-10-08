from fastapi import APIRouter
from app.user import routers as user_routers

api_router = APIRouter()

api_router.include_router(user_routers.router, tags=["user"], prefix="/users")