# AI Ecosystem Workspace

Workspace for the 241-353 AI Ecosystem Module.

## Structure

- `compose.yml` — Docker Compose setup running Redis, PostgreSQL, and Label Studio.
- `db/init/` — SQL scripts run automatically on first PostgreSQL boot (creates the `labelstudio` database).
- `.env.example` — Template for environment variables (copy to `.env` and set real secrets).
- `diagrams/` — Architecture diagrams (`overview.drawio`, `overview.png`).
- `work-result/` — Screenshots/results captured during development.

## Getting Started

1. Copy the environment template and set your own passwords:

   ```bash
   cp .env.example .env
   # then edit .env and change POSTGRES_PASSWORD / LABEL_STUDIO_PASSWORD
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

| Service       | Port / URL              | Notes                                              |
| ------------- | ----------------------- | -------------------------------------------------- |
| Redis         | `6379`                  | Cache / queue backend.                             |
| PostgreSQL    | `5432`                  | Central database. Holds `appdb` and `labelstudio`. |
| Label Studio  | http://localhost:8080   | Annotation tool. Uses the `labelstudio` database.  |

PostgreSQL runs a single instance serving two databases: `appdb` for the Central API
Server and `labelstudio` as the backend for Label Studio. Log in to Label Studio with
the `LABEL_STUDIO_USERNAME` / `LABEL_STUDIO_PASSWORD` values from your `.env`.

> **Note:** The init SQL under `db/init/` only runs the first time the PostgreSQL
> volume is created. If you already have a `postgresql-data` volume, recreate it with
> `docker compose down -v` (this deletes data) or create the `labelstudio` database
> manually.
