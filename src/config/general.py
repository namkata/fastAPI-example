import os
from pathlib import Path
from typing import Any
from functools import lru_cache
from pydantic import AnyUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict  # pydantic v2

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = ".env"
ENV_PATH = os.path.join(BASE_DIR, ENV_FILE)


class AppSettings(BaseSettings):
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

    DATABASE_URL: PostgresDsn | Any = "sqlite:///./sql_app.db"
    ALLOWED_HOSTS: set[AnyUrl] = ["*"]

    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"
        env_prefix = "app_"
        validate_assignment = True

    # model_config = SettingsConfigDict(env_file=ENV_PATH)


@lru_cache()
def get_app_settings() -> AppSettings:
    """
      This function returns a cached instance of the APPSettings object.

      Caching is used to prevent re-reading the environment every time the API settings are used in an endpoint.

      If you want to change an environment variable and reset the cache (e.g., during testing), this can be done
      using the `lru_cache` instance method `get_app_settings.cache_clear()`.
    """
    return AppSettings()
