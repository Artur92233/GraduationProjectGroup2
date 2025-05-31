FROM python:3.12-slim

WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
    JWT_SECRET="your-secret-key" \
    JWT_ALGORITHM="HS256"

RUN apt-get update \
    && apt-get install -y --no-install-recommends make

RUN pip install --upgrade pip \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-ansi --no-root --no-interaction

COPY /app /app

EXPOSE 25000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9999"]