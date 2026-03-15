from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    SECRET_KEY: str = "fallback-secret-key-please-change-in-production"
    DATABASE_URL: str = "sqlite:///./game_seer.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 天
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
