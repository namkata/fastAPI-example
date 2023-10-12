from fastapi import Request
from fastapi import APIRouter

home_router = APIRouter()


@home_router.get("/")
def home(request: Request):
    user = request.user
    print(request.user)
    return request.user.id
