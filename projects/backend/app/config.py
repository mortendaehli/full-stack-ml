import json
import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Config(BaseSettings):

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "full-stack-ml")
    SERVER_NAME: str = os.getenv("DOMAIN")
    SERVER_HOST: AnyHttpUrl = f"https://{SERVER_NAME}"
    API_V1_STR: str = "/api/v1"

    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", secrets.token_urlsafe(64))
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")
    JWT_EXPIRES: int = os.environ.get("JWT_EXPIRES", 30)
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ["true", "1"]

    SENTRY_DSN: Optional[HttpUrl] = os.getenv("SENTRY_DSN")

    PORT: int = os.environ.get("BACKEND_PORT_PORT", 8888)
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "prod")

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = list(json.loads(os.getenv("BACKEND_CORS_ORIGINS")))

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = os.getenv("SQLALCHEMY_DATABASE_URI")

    SMTP_TLS: bool = os.getenv("SMTP_TLS")
    SMTP_PORT: Optional[int] = os.getenv("SMTP_PORT")
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: Optional[EmailStr] = os.getenv("EMAILS_FROM_EMAIL")
    EMAILS_FROM_NAME: Optional[str] = os.getenv("EMAILS_FROM_NAME")

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
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

    @validator("SENTRY_DSN", pre=True, allow_reuse=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if not v:
            return None
        elif len(v) == 0:
            return None
        return v

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

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(values.get("SMTP_HOST") and values.get("SMTP_PORT") and values.get("EMAILS_FROM_EMAIL"))


config = Config()
