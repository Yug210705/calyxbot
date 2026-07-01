from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration via Pydantic BaseSettings.
    
    Reads from environment variables and `.env` files.
    Missing required variables will cause startup to fail with clear validation errors.
    """

    # Application Info
    PROJECT_NAME: str = "Calyx API"
    VERSION: str = "0.1.0"

    # Environment (affects logging, debugging, etc.)
    APP_ENV: Literal["development", "staging", "production"] = "development"

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Security / CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Supabase (Auth / Database)
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = Field(default=20)
    DB_MAX_OVERFLOW: int = Field(default=10)

    # Supabase Auth Configuration
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_JWT_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Dependency injection for settings.
    Uses lru_cache to ensure the Settings object is only instantiated once.
    """
    return Settings()
