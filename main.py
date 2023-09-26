from fastapi import FastAPI
from src.config.general import get_app_settings


def get_app() -> FastAPI:
    get_app_settings.cache_clear()
    settings = get_app_settings()
    my_app = FastAPI(**settings.fastapi_kwargs)
    # Include endpoint routes here:

    return my_app


app = get_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
