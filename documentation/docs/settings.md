## 📘 Конфігурація застосунку

Цей модуль зчитує змінні середовища та створює конфігураційний об'єкт для FastAPI-застосунку.  
Використовується, зокрема, для генерації рядка підключення до бази даних PostgreSQL у форматі `asyncpg`.
Фаїл [settings.py](..%2F..%2Fbackend_api%2Fapp%2Fsettings.py)

### 🔧 Основний код

```python
from functools import lru_cache
from pydantic_settings import BaseSettings


# ⚙️ Клас конфігурації, який автоматично зчитує змінні середовища
class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str

    @property
    def DATABASE_URL_ASYNC(self) -> str:
        """
        🔌 Формує рядок підключення до PostgreSQL для асинхронного драйвера asyncpg.

        Returns:
            str: Рядок підключення у форматі asyncpg.
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


# 🧠 Функція, що кешує конфігурацію для повторного використання
@lru_cache()
def get_settings() -> Settings:
    """
    📦 Повертає єдиний екземпляр налаштувань.

    Returns:
        Settings: Об'єкт налаштувань застосунку.
    """
    return Settings()


# 📌 Глобальний об'єкт налаштувань для імпорту в інших модулях
settings = get_settings()
