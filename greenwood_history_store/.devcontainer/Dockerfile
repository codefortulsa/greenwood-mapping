# https://github.com/devcontainers/images/tree/main/src/python
# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT=3.10-bullseye
FROM mcr.microsoft.com/devcontainers/python:${VARIANT} as base

# Install any build deps.
RUN apt-get -y update
RUN apt-get -y install postgis libpq-dev

ENV \
  # python
  PYTHONFAULTHANDLER=1 \
  PYTHONHASHSEED=random \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
   # pip
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=true \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_CACHE_DIR="/app/.cache" \
  VIRTUAL_ENV=/app/.venv

WORKDIR /app

ENV PATH "${VIRTUAL_ENV}/bin:${PATH}"

COPY pyproject.toml poetry.lock ./