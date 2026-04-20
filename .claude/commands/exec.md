---
description: Execute a command in a running container
---

Execute a command in a running container. Default to the `app` service (Django) unless the user specifies a different one.

Use: `docker compose exec <service> <command>`

Services: `app` (Django), `db` (postgis), `redis`, `martin` (once wired in).
