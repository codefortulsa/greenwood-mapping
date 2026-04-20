---
description: View logs from Docker containers
---

View and follow logs from Docker containers. If the user specifies a service name, show logs for that service only, otherwise show all logs.

Use: `docker compose logs -f <service?>`

Common services: `app` (Django), `db` (postgis), `redis`, `martin` (vector tile server — once wired in).
