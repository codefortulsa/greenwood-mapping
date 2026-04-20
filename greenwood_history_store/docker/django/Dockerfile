# Multi-stage Dockerfile.
#   base  — shared system deps + runtime tooling (no python deps yet)
#   dev   — installs all poetry groups; runs Django runserver with reload
#
# A `prod` stage will be added later with --only main + uvicorn. The
# compose file selects the target explicitly (`build.target: dev`) so
# production can drop in without touching the dev path.

# ---------------------------------------------------------------- base
FROM python:3.13-slim-bookworm AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry-cache

# System deps
#   libgdal-dev / gdal-bin -> django.contrib.gis needs libgdal at runtime
#   build-essential         -> needed to build any sdist-only wheels
#   gettext                 -> django i18n
RUN apt-get update && apt-get install --no-install-recommends -y \
      build-essential \
      libgdal-dev \
      gdal-bin \
      gettext \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==2.2.0"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# ---------------------------------------------------------------- dev
FROM base AS dev

# All groups (main + dev) so pytest / black / isort / ipykernel are
# available in the image. Bind-mount at runtime gives hot reload via
# Django's runserver.
RUN poetry install --no-root

COPY . .

COPY docker/django/start.sh /usr/local/bin/start
RUN chmod +x /usr/local/bin/start

EXPOSE 8000
CMD ["start"]
