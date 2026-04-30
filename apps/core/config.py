from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Literal

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".envs/.env.local",
        env_ignore_empty=True,
        extra="ignore",
    )
    # project settings

    API_V1_STR: str = ""
    PROJECT_NAME: str = ""
    PROJECT_DESCRIPTION: str = ""
    SITE_NAME: str = ""
    # database settings
    DATABASE_URL: str

    @property
    def DATABASE_URL(self):
        if self.DATABASE_URL:
            return self.DATABASE_URL


settings = Settings()
