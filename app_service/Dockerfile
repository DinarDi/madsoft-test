FROM python:3.12-alpine3.20

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN mkdir app_service
WORKDIR /app_service

COPY pyproject.toml ./poetry.lock ./

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

COPY . /app_service