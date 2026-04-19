"""Centralised application settings via pydantic-settings.

Every environment variable used by the app MUST be declared here.
database.py, main.py, routers and services import settings
instead of calling os.getenv directly.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -- Database
    DATABASE_URL: str = "postgresql+asyncpg://braslina:braslina_dev@localhost:5432/braslina"

    # -- Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # -- MinIO
    MINIO_ENDPOINT: str = "localhost:9002"
    MINIO_ACCESS_KEY: str = "braslina"
    MINIO_SECRET_KEY: str = "braslina_dev"
    MINIO_BUCKET: str = "braslina-screenshots"
    MINIO_SECURE: bool = False

    # -- n8n
    N8N_BASE_URL: str = "http://localhost:5680"

    # -- Monitor agent
    ALERT_THRESHOLD_PCT: float = 5.0

    # -- App
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    BRASLINA_API_KEY: str = ""


settings = Settings()
