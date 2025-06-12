FROM python:3.12-slim

# Устанавливаем Poetry и базовые зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction

# Копируем весь проект
COPY . .

# Открываем порт (если нужно)
EXPOSE 12346

# Запуск приложения
CMD ["poetry", "run", "uvicorn", "main:app", "--host=0.0.0.0", "--port=12346", "--reload"]