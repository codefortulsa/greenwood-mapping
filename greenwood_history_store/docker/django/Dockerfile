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

# Install Poetry in a dedicated location so it's not on the app venv
RUN pip install --no-cache-dir "poetry==2.2.0"

WORKDIR /app

# Copy lockfiles first so dep install is cached until pyproject.toml / poetry.lock change
COPY pyproject.toml poetry.lock ./
# Install all groups (main + dev) so tests/format/lint work out of the box.
# Prod builds should switch this to `--only main` in a separate stage.
RUN poetry install --no-root

# Copy app code
COPY . .

# Dev start script
COPY docker/django/start.sh /usr/local/bin/start
RUN chmod +x /usr/local/bin/start

EXPOSE 8000
CMD ["start"]
