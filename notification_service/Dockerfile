FROM python:3.13-slim

WORKDIR /app

ENV POETRY_NO_INTERACTION=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends make

#ENV PYTHONFAULTHANDLER=1 \
#    PYTHONHASHSEED=random \
#    PYTHONUNBUFFERED=1 \
#    POETRY_VIRTUALENVS_CREATE=false \
#    POETRY_NO_INTERACTION=1 \
#    PIP_NO_CACHE_DIR=1

RUN pip install --upgrade pip \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-ansi --no-root --no-interaction

COPY /app /app