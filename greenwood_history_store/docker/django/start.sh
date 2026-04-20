#!/bin/bash
set -euo pipefail

# Migrations are run explicitly via `just manage migrate` (or
# `just bootstrap`). During the schema rebuild phase the migration
# set is in flux, so running them unconditionally on start just
# causes startup failures. Re-enable this once migrations settle.
exec python manage.py runserver 0.0.0.0:8000
