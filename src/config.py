from typing import Any

from pydantic import BaseSettings, PostgresDsn

from src.constants import Environment


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn

    ENVIRONMENT: Environment = Environment.PRODUCTION

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None
    CORS_HEADERS: list[str]

    APP_VERSION: str = "1"


settings = Config()

app_configs: dict[str, Any] = {"title": "DressUp API"}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

# if not settings.ENVIRONMENT.is_debug:
#     app_configs["openapi_url"] = None  # hide docs
