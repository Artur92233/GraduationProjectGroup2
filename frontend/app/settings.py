from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DEBUG: bool = False
    BACKEND_API: str
    ACCESS_KEY: str
    SECRET_KEY: str
    BUCKET_NAME: str
    ENDPOINT: str
    PUBLIC_URL: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
