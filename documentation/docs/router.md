## 📘 Маршрути користувачів

Цей модуль містить маршрути, пов’язані з реєстрацією користувачів.  
На поточному етапі реалізовано базовий маршрут створення, який повертає дані без збереження в базу.
Фаїл [router.py](..%2F..%2Fbackend_api%2Fapp%2Fapplications%2Fusers%2Frouter.py)

### 🔧 Основний код

```python
from fastapi import APIRouter, status

from applications.users.schemas import BaseFields, RegisterUserFields

# 📍 Ініціалізуємо роутер для користувачів
router_users = APIRouter()

@router_users.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: RegisterUserFields) -> BaseFields:
    """
    ➕ Створення нового користувача (заглушка).

    Приймає дані користувача та повертає їх без обробки.

    Args:
        new_user (RegisterUserFields): Вхідні дані для нового користувача.

    Returns:
        BaseFields: Ті ж самі дані, без змін.
    """
    return new_user
