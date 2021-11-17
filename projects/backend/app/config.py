import json
import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, PostgresDsn, validator


class Config(BaseSettings):

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "full-stack-ml")
    API_V1_STR: str = "/api/v1"

    DOMAIN: str = os.getenv("DOMAIN")
    BACKEND_URL: AnyHttpUrl = f"https://api.{os.getenv('DOMAIN')}"

    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ["true", "1"]
    PORT: int = os.environ.get("BACKEND_PORT_PORT", 8888)
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")

    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", secrets.token_urlsafe(64))
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")
    JWT_EXPIRES: int = os.environ.get("JWT_EXPIRES", 30)

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = list(json.loads(os.getenv("BACKEND_CORS_ORIGINS")))

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = os.getenv("SQLALCHEMY_DATABASE_URI")

    FIRST_SUPERUSER: EmailStr = os.getenv("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")
    USERS_OPEN_REGISTRATION: bool = False

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


config = Config()
