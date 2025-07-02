## 📘 Налаштування Alembic для міграцій бази даних

Цей модуль відповідає за конфігурацію та запуск міграцій бази даних  
в режимах offline (без підключення до бази) та online (з підключенням).
Фаїл [env.py](..%2F..%2Fbackend_api%2Fapp%2Fmigrations%2Fenv.py)

### 🔧 Основний код

```python
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# 📁 Отримуємо об'єкт конфігурації Alembic
config = context.config

# ⚙️ Налаштовуємо логування з файлу конфігурації
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🧩 Метадані моделей для автогенерації міграцій
target_metadata = None

def run_migrations_offline() -> None:
    """
    🛠 Виконує міграції в offline-режимі.

    - Конфігурує Alembic з URL бази даних без створення з'єднання.
    - Підходить, коли немає прямого доступу до бази.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    🛠 Виконує міграції в online-режимі.

    - Створює підключення до бази даних.
    - Виконує міграції з використанням живого з'єднання.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# 🚦 Визначаємо режим і запускаємо відповідну функцію
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
