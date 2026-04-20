---
description: Run Django management commands
---

Execute Django management commands:
`docker compose run --rm app poetry run python manage.py <command>`

Common commands:
- `migrate` — run database migrations
- `makemigrations` — create new migrations
- `showmigrations` — view migration state
- `createsuperuser` — create a Django admin user
- `shell_plus` — shell with models auto-imported (see also `/shell`)
- `test` — run Django's test runner (prefer `/test` for pytest)
- `collectstatic` — gather static files
- `import_data` — project-specific: import residents/businesses CSVs
- `import_polk` — (once implemented) import Polk city-directory xlsx files
- `import_geojson` — (once implemented) load GeoJSON assets into overlays

Use the exact command the user requests.
