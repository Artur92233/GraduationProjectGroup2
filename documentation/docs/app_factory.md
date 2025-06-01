## 📘 Ініціалізація FastAPI-застосунку

Цей модуль створює та конфігурує екземпляр FastAPI-застосунку.  
Він включає маршрути для роботи з користувачами за шляхом.
Фаїл [app_factory.py](..%2F..%2Fbackend_api%2Fapp%2Fapp_factory.py)

### 🔧 Основний код

```python
from fastapi import FastAPI

# 📥 Імпортуємо роутер з модуля користувачів
from applications.users.router import router_users

def get_application() -> FastAPI:
    """
    🏁 Створює та повертає налаштований FastAPI застосунок.

    - Встановлює префікс `/api` для всіх маршрутів.
    - Додає маршрути, пов’язані з користувачами, з префіксом `/users`.
    - Додає теги для групування в документації Swagger.

    Returns:
        FastAPI: Сконфігурований застосунок FastAPI.
    """
    app = FastAPI(root_path="/api", root_path_in_servers=True)

    # 🔗 Підключаємо роутер користувачів: /api/users
    app.include_router(router_users, prefix="/users", tags=["Users"])

    return app
