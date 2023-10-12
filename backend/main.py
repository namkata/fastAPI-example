import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from logging.config import fileConfig
# from core.exceptions.handlers import CustomException, http_exception_handler
from core.config import settings, get_settings, LOGGING_CONFIG_FILE, SQLITE_DB_URL
from fastapi_sqlalchemy import DBSessionMiddleware
from db.base_class import Base
from db.session import engine
from api.router import router

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
    my_app.include_router(router, prefix=settings.api_str)
    # my_app.add_exception_handler(CustomException, http_exception_handler)
    return my_app


app = get_app()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=settings.port, reload=True)
