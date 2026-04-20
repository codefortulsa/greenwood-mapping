---
description: Create and run Django migrations
---

Handle Django database migrations. Ask the user what they want, or do the requested action directly if they specify:

1. Create new migrations: `docker compose run --rm app poetry run python manage.py makemigrations`
2. Run migrations: `docker compose run --rm app poetry run python manage.py migrate`
3. Show migration status: `docker compose run --rm app poetry run python manage.py showmigrations`
4. For a specific app: append `<app_name>` to `makemigrations` / `migrate`.

For **iterative model changes where uncommitted migrations should be reset**, use `/migrate-smart` instead.
