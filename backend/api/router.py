from fastapi import APIRouter
from api.routes import login, users, items

router = APIRouter()
router.include_router(login.router, tags=["login"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(items.router, prefix="/items", tags=["items"])
