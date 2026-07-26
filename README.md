# AI Ecosystem Workspace

Workspace for the 241-353 AI Ecosystem Module.

## Structure

- `compose.yml` — Docker Compose setup running Redis, PostgreSQL, Label Studio, and MinIO. All services share a centralized logging config (`x-logging` anchor: `json-file` driver, 10 MB per file, 3 files kept).
- `db/init/` — SQL scripts run automatically on first PostgreSQL boot (creates the `labelstudio` database).
- `.env.example` — Template for environment variables (copy to `.env` and set real secrets).
- `diagrams/` — Architecture diagrams (`overview.drawio`, `overview.png`).
- `work-result/` — Screenshots/results captured during development.
- `backend/` — Python backend.
  - `core/config.py` — Pydantic `Settings` (env vars for Postgres, Label Studio, MinIO, logging).
  - `core/logger.py` — Custom `get_logger()` factory: console + rotating file handler (`backend/logs/app.log`).
  - `sandbox/` — Standalone test/demo scripts (Redis, Label Studio, custom logger, `minio/` upload-download and versioning tests).

## Getting Started

1. Copy the environment template and set your own passwords:

   ```bash
   cp .env.example .env
   # then edit .env and change POSTGRES_PASSWORD / LABEL_STUDIO_PASSWORD / MINIO_ROOT_PASSWORD
   ```

2. Start the stack:

   ```bash
   docker compose up -d
   ```

3. Check that everything is healthy:

   ```bash
   docker compose ps
   ```

## Services

| Service       | Port / URL                                      | Notes                                              |
| ------------- | ------------------------------------------------ | --------------------------------------------------- |
| Redis         | `6379`                                            | Cache / queue backend.                             |
| PostgreSQL    | `5432`                                            | Central database. Holds `appdb` and `labelstudio`. |
| Label Studio  | http://localhost:8080                             | Annotation tool. Uses the `labelstudio` database.  |
| MinIO         | http://localhost:9000 (API) / `:9001` (Console)   | S3-compatible object storage.                      |

PostgreSQL runs a single instance serving two databases: `appdb` for the Central API
Server and `labelstudio` as the backend for Label Studio. Log in to Label Studio with
the `LABEL_STUDIO_USERNAME` / `LABEL_STUDIO_PASSWORD` values from your `.env`. Log in to
the MinIO Console with `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`.

> **Note:** The init SQL under `db/init/` only runs the first time the PostgreSQL
> volume is created. If you already have a `postgresql-data` volume, recreate it with
> `docker compose down -v` (this deletes data) or create the `labelstudio` database
> manually.

## Logging

- **Application logs** — `backend/core/logger.py` exposes `get_logger(name)`, used across
  the backend for consistent DEBUG/INFO/WARNING/ERROR/CRITICAL logging. Each logger writes
  to the console and to a rotating file at `backend/logs/app.log` (rotates at 1 MB, keeps
  3 backups — configurable via `core/config.py`).
- **Container logs** — every service in `compose.yml` shares the `x-logging` anchor, so
  Docker's `json-file` driver rotates each container's logs at 10 MB, keeping 3 files.
  View combined logs with:

  ```bash
  docker compose logs -f
  ```
