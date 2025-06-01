## 📘 Pydantic-схеми користувача

Цей модуль містить Pydantic-моделі для валідації та опису структури вхідних і вихідних даних, пов’язаних з користувачами.
Фаїл [schemas.py](..%2F..%2Fbackend_api%2Fapp%2Fapplications%2Fusers%2Fschemas.py)

### 🔧 Основний код

```python
from pydantic import BaseModel, EmailStr, Field, ValidationInfo, model_validator


# 📄 Базова схема користувача: ім’я та email
class BaseFields(BaseModel):
    email: EmailStr = Field(description="User email", examples=["live.here@gmail.com"])
    name: str = Field(description="User nickname", examples=["George"])


# 🔐 Окрема схема для пароля з кастомною валідацією
class PasswordField(BaseModel):
    password: str = Field(min_length=8)

    @model_validator(mode="before")
    def validate_password(cls, values: dict, info: ValidationInfo) -> dict:
        """
        🛡 Валідація пароля перед ініціалізацією об'єкта.

        - Перевіряє, що пароль не порожній.
        - Має довжину щонайменше 8 символів.
        - Не містить пробілів.
        """
        password = (values.get("password") or "").strip()
        if not password:
            raise ValueError("Password required")

        if len(password) < 8:
            raise ValueError("Too short password")

        if " " in password:
            raise ValueError("No spaces in password, please")

        return values


# 🧾 Комбінована схема для реєстрації користувача
class RegisterUserFields(BaseFields, PasswordField):
    """
    📦 Об'єднує базові дані користувача та пароль.

    Використовується при створенні нового користувача.
    """
    pass
