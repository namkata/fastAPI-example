from fastapi import APIRouter
from api.routes import login, users, items, home

router = APIRouter()
router.include_router(login.router, tags=["login"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(home.home_router, prefix="/home", tags=["home"])
