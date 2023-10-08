import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from logging.config import fileConfig
from core.exceptions.handlers import CustomException, http_exception_handler
from settings.config import settings, get_settings, LOGGING_CONFIG_FILE, SQLITE_DB_URL
from fastapi_sqlalchemy import DBSessionMiddleware
from app.api.models import Base
from core.db.base import engine
from app.api.routers import api_router

# Configure logging
fileConfig(LOGGING_CONFIG_FILE, disable_existing_loggers=False)
Base.metadata.create_all(bind=engine)


def get_app() -> FastAPI:
    get_settings.cache_clear()
    my_app = FastAPI(**settings.fastapi_kwargs)
    my_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.accept_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    my_app.add_middleware(DBSessionMiddleware, db_url=settings.database_url or SQLITE_DB_URL)
    # Include endpoint routes here:
    my_app.include_router(api_router, prefix=settings.api_str)
    my_app.add_exception_handler(CustomException, http_exception_handler)
    return my_app


app = get_app()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=settings.port, reload=True)
