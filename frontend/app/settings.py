from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DEBUG: bool = False
    BACKEND_API: str



@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()