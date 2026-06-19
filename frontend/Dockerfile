FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends make curl gettext \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && mv /root/.local/bin/uvx /usr/local/bin/uvx

COPY pyproject.toml uv.lock /app/

RUN uv pip install --system --no-cache .

COPY /app /app
EXPOSE 12346

# Запуск приложения
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=12346", "--reload"]