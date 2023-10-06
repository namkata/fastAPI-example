import os
from pathlib import Path
import secrets
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, EmailStr, PostgresDsn, RedisDsn

# See more in here:
# https://fastapi.tiangolo.com/advanced/settings/#__tabbed_5_1

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ".env"
ENV_PATH = os.path.join(BASE_DIR, ENV_FILE)


class Settings(BaseSettings):
    # API Settings
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI"
    version: str = "0.1.0"
    # Custom settings
    disable_docs: bool = False
    api_str: str = "api/v1"
    secret_key: str = secrets.token_urlsafe(32)
    server_domain: AnyHttpUrl = "http://127.0.0.1:8000"
    accept_cors_origins: List[AnyHttpUrl] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # celery configure
    celery_broker_url: RedisDsn = "redis://localhost:6379"
    celery_result_backend: RedisDsn = "redis://localhost:6379"

    # SMTP configure
    smtp_tls: bool = True
    smtp_port: Optional[int] = None
    smtp_host: Optional[str] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_default_email: Optional[EmailStr] = None
    smtp_enable: bool = False

    # database configure
    database_url: Optional[PostgresDsn] = None
    database_enable: bool = False

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        fastapi_kwargs: dict[str, Any] = {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }
        if self.disable_docs:
            fastapi_kwargs.update({"docs_url": None, "openapi_url": None, "redoc_url": None})
        return fastapi_kwargs

    # Note: Version 2
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        env_prefix="app_",  # Variable start with APP_ in .env file. e.g: APP_DEBUG=False
        validate_assignment=True
    )

    # Note: Version 1
    #     class Config:
    #         env_file = ENV_PATH
    #         env_file_encoding = "utf-8"
    #         env_prefix = "app_"
    #         validate_assignment = True


@lru_cache()
def get_settings() -> Settings:
    """
       This function returns a cached instance of the Settings object.

       Caching is used to prevent re-reading the environment every time the API settings are used in an endpoint.

       If you want to change an environment variable and reset the cache (e.g., during testing), this can be done
       using the `lru_cache` instance method `get_settings.cache_clear()`.
    """
    return Settings()


settings = get_settings()
