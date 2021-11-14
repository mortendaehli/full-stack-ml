# syntax=docker/dockerfile:1
FROM python:3.9 as dev

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
  apt-get -y upgrade && \
  rm -rf /var/lib/apt/lists/* && \
  pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir poetry

WORKDIR /libraries/imagenet/

COPY libraries/imagenet/pyproject.toml libraries/imagenet/poetry.lock ./

# Building all dependencies first to get a python environment we can use for dev
RUN pip install --upgrade pip poetry && poetry config virtualenvs.create false && poetry install --no-root

FROM dev AS build

# Then the app afterwards.
COPY libraries/imagenet/ ./

RUN pip install --upgrade pip poetry && poetry config virtualenvs.create false && poetry install

FROM build AS tests

RUN poetry run pytest tests
