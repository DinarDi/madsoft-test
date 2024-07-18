FROM python:3.12-alpine3.20

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN mkdir media_service
WORKDIR /media_service

COPY pyproject.toml ./poetry.lock ./

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

COPY . /media_service