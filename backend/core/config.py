# backend/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",         # backend/.env (run scripts from the backend/ dir)
        env_file_encoding="utf-8",
        extra="ignore",          # Ignore extra environment variables not defined in Settings
    )

    # PostgreSQL — matches the .env used by compose.yml
    postgres_user: str = "aieco"
    postgres_password: str = "change_me"
    postgres_db: str = "appdb"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379

    # Label Studio
    label_studio_url: str = "http://localhost:8080"
    label_studio_api_key: str = ""

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

settings = Settings()