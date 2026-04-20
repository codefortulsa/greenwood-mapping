# Stack direction and upgrade plan

Captures the agreed-upon target stack and the phased work to get there.
Notes are scoped to things that aren't obvious from code/config — refer to
`CLAUDE.md` and `greenwood_history_store/README.md` for the as-is state.

## Target stack

- **Postgres / PostGIS** — latest (PostGIS 17 / PG 17). Current: PostGIS
  14-master in `greenwood_history_store/.devcontainer/docker-compose.yaml`.
- **Python** — latest (3.12+). Current: `python = "^3.10"` in `pyproject.toml`.
- **Django** — latest (5.x). Current: `^4.2` (bumped from 4.1 in the WIP
  preservation commits).
- **pydantic** — v2. Current: v1. Note: `django-pydantic-field` had a
  breaking API change for pydantic v2 (moved to v0.3+). `BuildingMeta` in
  `apps/buildings/models.py` will need review.
- **Poetry** — latest (2.x). Lock regenerated as part of the upgrade pass.
- **Martin** — `ghcr.io/maplibre/martin:latest`, serving MVT tiles from a
  PostGIS function source. See below.
- **Frontend** — React + react-map-gl (MapLibre GL under the hood).
  Replaces the static `map_mvp/` Mapbox GL HTML (currently gitignored).
  Martin URLs are consumed directly; Django exposes data APIs only.

## Bootstrap goal

One-command bring-up that:

1. Starts postgres/postgis, martin, redis, and the Django app
2. Runs Django migrations
3. Imports shapefiles under `data/shape/` via `shp2pgsql`
4. Imports Polk city directories (`data/Combined_PolkDirectory_{1920-1922}.xlsx`)
5. Exposes martin at `:3000` and Django at `:8000`

## Martin architecture

Pattern adopted from a sibling Django project already running Martin
against PostGIS (see memory: "Reference repos for stack patterns" for
the concrete path/branch).

Key pattern:

- PostGIS function source (`CREATE FUNCTION area_tiles(z, x, y, query_params)
  RETURNS bytea`) returning `ST_AsMVT(...)`. Not materialized tiles.
- Tiles carry **geometry + metadata only** — time-varying values (entities,
  residents per year) come from Django APIs and are joined client-side via
  MapLibre `setFeatureState`.
- Martin config in `./martin/config.yaml` mounted as `/config` in the
  container, `auto_publish: false` so only curated function sources are
  exposed.
- Rationale: geometry cache hit rate stays high; changing the displayed
  year/entity doesn't re-fetch tiles.

For greenwood the initial function sources will likely be:

- `parcel_tiles(z, x, y, params)` — over the `parcels` table (currently
  unmanaged, see `apps/shapes/models.py`)
- `plot_tiles(z, x, y, params)` — for any future custom plot outlines
- possibly `street_tiles(...)` if we want to render historical street grids

Time-scoped querying (entities/addresses by year) stays in the Django
data API, filtered via `TimeRange.objects.date_in(...)`.

## Tooling conventions

- **`justfile`** replaces the existing `greenwood_history_store/makefile`.
  Keep the `shp2pgsql` targets and add `up/down/logs/manage/prune/migrate/
  test/format/lint` one-liners that wrap `docker compose`.
- **`.claude/` convention** (per user directive):
  - `.claude/docs/` — project-local design docs, upgrade plans, references.
  - `.claude/skills/` — custom skills developed for this project.
  - `.claude/settings.local.json` — gitignored; per-developer.
  - Other `.claude/settings.json` / `commands/` / `agents/` / `hooks/` may be
    added when needed.

## Phased upgrade plan

1. **WIP preservation** — done. `import-test` now carries LFS setup, source
   data under LFS, the new `time_ranges` app, API/admin enhancements, the
   4.1→4.2 interim bumps, `CLAUDE.md`, and scratch `temp.py`.
2. **Audit baseline** — run existing tests, map working vs half-finished
   features, document notebook import flow.
3. **Dependency upgrade** — do it in small steps, each independently tested:
   Python 3.10→3.12, Django 4.2→5.x, pydantic 1→2 (touches
   `django-pydantic-field` and `BuildingMeta`), Poetry 1.x→2.x,
   postgis/postgis 14→17.
4. **Dockerization** — rewrite dev container / compose so the whole stack
   (db, redis, martin, django) comes up with one command and bootstraps from
   `data/`.
5. **Martin wiring** — add martin service, author function sources, verify
   MVT tiles end to end.
6. **React frontend** — new app (probably replacing `map_mvp/`) using
   react-map-gl, pointing at martin for tiles and Django for data.

Keep phases small and reviewable; each should leave the repo working.
