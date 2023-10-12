from typing import List

import uvicorn
from fastapi import FastAPI, Depends
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from logging.config import fileConfig
from core.config import settings, get_settings, LOGGING_CONFIG_FILE, SQLITE_DB_URL
from fastapi_sqlalchemy import DBSessionMiddleware
from db.base_class import Base
from db.session import engine
from api.router import router
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from core.exceptions import CustomException
from middlewares.authentication import AuthenticationMiddleware, AuthBackend
from middlewares.response_log import ResponseLogMiddleware
import dependencies

# Configure logging
fileConfig(LOGGING_CONFIG_FILE, disable_existing_loggers=False)
Base.metadata.create_all(bind=engine)


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(ResponseLogMiddleware),
        Middleware(
            DBSessionMiddleware,
            db_url=settings.database_url or SQLITE_DB_URL
        )
    ]
    return middleware


def get_app() -> FastAPI:
    get_settings.cache_clear()
    my_app = FastAPI(
        **settings.fastapi_kwargs,
        dependencies=[Depends(dependencies.Logging)],
        middleware=make_middleware()
    )
    # my_app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=settings.accept_cors_origins,
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )
    # my_app.add_middleware(DBSessionMiddleware, db_url=settings.database_url or SQLITE_DB_URL)
    # Include endpoint routes here:
    my_app.include_router(router, prefix=settings.api_str)
    # my_app.add_exception_handler(CustomException, http_exception_handler)
    return my_app


app = get_app()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=settings.port, reload=True)
