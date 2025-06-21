from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    RMQ_HOST: str
    RMQ_PORT: int
    RMQ_VIRTUAL_HOST: str
    RMQ_USER: str
    RMQ_PASSWORD: str

    TOKEN_UKR_NET: str
    USER: str
    SMTP_SERVER: str

@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
