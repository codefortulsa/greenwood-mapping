---
description: Smart migration handling for Django apps (reset uncommitted migrations cleanly)
---

You are helping with Django migrations in a smart way. Follow these steps:

1. **Detect context from conversation**: If the user mentions clearing, resetting, redoing, or fresh starting migrations, proceed with the smart reset flow. Otherwise, just run normal migrations (prefer `/migrations`).

2. **For smart reset flow**:

   a. Ask which app the user is working on if not clear from context (check recent file edits in `greenwood_history_store/greenwood_history/apps/*/models.py`).

   b. Find uncommitted migration files for that app:
      - Run: `git status --porcelain greenwood_history_store/greenwood_history/apps/<app_name>/migrations/*.py`
      - Look for files marked with `??` (untracked) or `M ` (modified).

   c. If uncommitted migrations exist:
      - Get the last committed migration: `git ls-files greenwood_history_store/greenwood_history/apps/<app_name>/migrations/*.py | sort | tail -1`
      - Extract the migration number (e.g., `0001`, `0002`) from the filename.
      - Migrate backward to that migration: `docker compose run --rm app poetry run python manage.py migrate <app_name> <migration_number>`
      - Delete the uncommitted migration files: `rm greenwood_history_store/greenwood_history/apps/<app_name>/migrations/00*.py` (only uncommitted ones — list them first and confirm).
      - Create fresh migrations: `docker compose run --rm app poetry run python manage.py makemigrations <app_name>`
      - Run the new migrations: `docker compose run --rm app poetry run python manage.py migrate <app_name>`

   d. If no uncommitted migrations, just:
      - `makemigrations <app_name>` then `migrate <app_name>`.

3. **For normal migration flow**:
   - Run: `docker compose run --rm app poetry run python manage.py migrate`

**Important notes**:
- Only delete migration files that are **uncommitted** (shown by `git status`). Never delete committed migrations.
- If migrating backward fails, explain the issue and ask whether to flush the database (destructive — prefer `/prune` + `just bootstrap`).
- Show the user what you're doing at each step.
- This command applies after the initial migration rebuild; during the upgrade pass (zeroing out all migrations), follow the plan in `.claude/docs/schema-redesign.md` instead.
