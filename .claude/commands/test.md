---
description: Run tests
---

Run the test suite via pytest. If the user specifies a path or app, scope to that; otherwise run everything.

Use: `docker compose run --rm app poetry run pytest <args>`

Pytest config lives in `greenwood_history_store/pyproject.toml` — it sets `DJANGO_CONFIGURATION=Test` automatically.
