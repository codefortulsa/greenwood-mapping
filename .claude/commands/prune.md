---
description: Remove containers and volumes
---

Stop and remove all containers and their volumes. This is a destructive operation that deletes all data in the database and other volumes.

Warn the user about data loss and ask for confirmation before running:
`docker compose down -v`

Note: the repo includes a `just bootstrap` recipe that re-creates a seeded DB quickly after a prune. Mention this to the user when confirming.
