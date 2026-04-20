---
description: Open PostgreSQL database shell
---

Open a psql shell in the postgis container:
`docker compose exec db psql -U postgres -d greenwood_history`

PostGIS extensions are active (see `CREATE EXTENSION postgis` in the image's init). Useful one-offs:
- `\dt` — list tables
- `\d <table>` — describe table
- `SELECT ST_AsText(geom) FROM parcels LIMIT 5;` — inspect geometry
