# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose

An interactive historical map/timeline of the Greenwood neighborhood in Tulsa, OK (pre- and post-1921 Tulsa Race Massacre). The repo holds a relational data store that unifies fragmented source data (Polk city directories, census, land records, fire insurance maps, parcel shapes) so it can be queried by address/entity across time.

## Top-level layout

- `greenwood_history_store/` — the primary, actively developed component. A Django + PostGIS data store exposing a DRF API. **This is where nearly all work happens.**
- `map_mvp/` — static Mapbox GL HTML demo. Gitignored (see `.gitignore`). Not wired to the backend.
- `pdf_import/` — placeholder, empty.

When the user says "the app" or gives an unqualified Django/Python instruction, assume `greenwood_history_store/`.

## Development environment

Development is intended to happen inside the VS Code devcontainer (`greenwood_history_store/.devcontainer/`), which provisions three services:

- `app` — Python 3.10 + Poetry, mounted at `/app`
- `db` — `postgis/postgis:14-master` (PostGIS is required; several models use `django.contrib.gis`)
- `redis` — cache backend

The container sets `DJANGO_CONFIGURATION=Dev` and `DATABASE_URL=postgis://...`. `postCreateCommand` runs `poetry install`.

Settings use **django-configurations**: `DJANGO_SETTINGS_MODULE=greenwood_history.config` plus `DJANGO_CONFIGURATION=Dev|Prod|Test` selects the class in `greenwood_history/config/{dev,prod,test}.py`. All three extend `Common` in `common.py`. A `SECRET_KEY` env var is required (it's a `values.SecretValue()`).

## Common commands

All commands run from `greenwood_history_store/` unless noted.

```bash
# Django management — note the double ./ invocation via poetry
poetry run python ./manage.py migrate
poetry run python ./manage.py runserver
poetry run python ./manage.py makemigrations
poetry run python ./manage.py import_data   # custom cmd, imports data/residents.csv

# Tests (pytest-django; config in pyproject.toml uses DJANGO_CONFIGURATION=Test)
poetry run pytest
poetry run pytest greenwood_history/apps/addresses/tests/test_models.py::test_parse_street_name

# Formatting
poetry run black .
poetry run isort .
```

GIS shapefile import is driven by the `makefile` (uses host `shp2pgsql` + `psql`):

```bash
make parcels     # imports data/shape/Parcels_20220929/PARCELS220929.shp
make quarters
make townships
make models      # regenerates apps/shapes/models.py via `manage.py inspectdb`
make all         # parcels + quarters + townships + models
```

The shape tables are unmanaged (`managed = False` in `apps/shapes/models.py`) — Django does not own their schema; only `shp2pgsql` does. Regenerate `shapes/models.py` with `make models` after re-importing shapes.

## Architecture

### Apps (under `greenwood_history/apps/`)

The `apps/` directory is added to `sys.path` in `common.py`, so imports are **bare** (`from entities.models import Entity`, not `from greenwood_history.apps.entities...`). Maintain this convention.

- **`entities`** — polymorphic people/businesses. `Entity` (via `django-polymorphic`) is the base; `Person` and `Business` inherit. `Entity.canonical` is a self-FK used to merge duplicates/aliases (same person appearing under different names across source years). `Person.meta` stores a parsed name dict (via `nameparser.HumanName`), refreshed on `save()`.
- **`addresses`** — `Street` + `Address`. Data sources are messy, so both models have `get_or_create_from_*` classmethods that normalize input: `Street.get_or_create_from_name` parses strings like `"aardvark-N Ave."` via the `street_pattern` regex + `parse_street_name`; `Address.get_or_create_from_unique` splits building numbers from trailing letters/"rear" suffixes. Prefer these over raw `get_or_create` when ingesting source data.
- **`time_ranges`** — `TimeRange` + `EntityAddressTimeRangeThrough`. This is the **core join**: (entity, address, time_range) triples record who lived/worked where during which period (e.g. "1920 directory"). Query by date via `TimeRange.objects.date_in(datetime)`.
- **`buildings`** — `Building` with a PostGIS `PolygonField` outline, FK to `Address`, and a pydantic `BuildingMeta` (style, floors) persisted via `django_pydantic_field.SchemaField`.
- **`shapes`** — unmanaged GIS tables (`Parcels`, `Quarters`, `Townships`) populated by the `makefile`.
- **`plots`** — largely empty scaffold.

### Change tracking

`Entity`, `Person`, and `Business` are wrapped with `@pghistory.track(pghistory.Snapshot(), ...)` to write audit rows on every change (see `pghistory.admin` registered in `INSTALLED_APPS`). `Entity.Meta.triggers` uses `pgtrigger` to make `name` read-only post-insert and to block deletes — this is intentional: historical data shouldn't be rewritten or lost. Don't "fix" these by removing the triggers.

### API

DRF viewsets registered in `greenwood_history/urls.py` via a `DefaultRouter`: `/entities`, `/addresses`, `/streets`, plus `/admin/`. `AddressViewSet` exposes filter fields on the related `street`. Pagination + `DjangoFilterBackend` + `SearchFilter` are on by default (`REST_FRAMEWORK` in `common.py`).

### Data flow

Source spreadsheets/CSVs live in `data/` (Polk directories 1920–1922, `residents.csv`, `businesstrr.csv`, `shape/` for shapefiles). The typical import path is: normalize raw row → `Street.get_or_create_from_name` → `Address.get_or_create_from_unique` → create/lookup `Entity` → attach `EntityAddressTimeRangeThrough` to a `TimeRange`. The `import_data` management command and notebooks in `notebooks/` (`polk_import.ipynb`, `import_test.ipynb`) are the working examples.
