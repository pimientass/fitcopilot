from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = Field(default="dev", alias="APP_ENV")
    app_name: str = Field(default="fitcopilot", alias="APP_NAME")

    db_path: Path = Field(default=Path("data/app.db"), alias="DB_PATH")

    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="qwen3:4b", alias="OLLAMA_MODEL")
    ollama_timeout_seconds: int = Field(default=60, alias="OLLAMA_TIMEOUT_SECONDS")
    ollama_keep_alive: str = Field(default="5m", alias="OLLAMA_KEEP_ALIVE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
