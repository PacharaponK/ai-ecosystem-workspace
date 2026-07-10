# AI Ecosystem Workspace

Workspace for the 241-353 AI Ecosystem Module.

## Structure

- `compose.yml` — Docker Compose setup running Redis, PostgreSQL, and Label Studio.
- `db/init/` — Optional SQL scripts run automatically on first PostgreSQL boot (empty for now; drop `*.sql` here to bootstrap extra databases/roles).
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

| Service       | Port / URL              | Notes                                             |
| ------------- | ----------------------- | ------------------------------------------------- |
| Redis         | `6379`                  | Cache / queue backend.                            |
| PostgreSQL    | `5432`                  | Central database. Hosts the `labelstudio` database. |
| Label Studio  | http://localhost:8080   | Annotation tool. Uses the `labelstudio` database. |

PostgreSQL auto-creates the `LABEL_STUDIO_DB` database (`labelstudio`) on first boot,
which Label Studio uses as its backend. Log in to Label Studio with the
`LABEL_STUDIO_USERNAME` / `LABEL_STUDIO_PASSWORD` values from your `.env`.

> **Note:** When the Central API Server needs its own database later, add a
> `CREATE DATABASE ...` script under `db/init/` and recreate the volume with
> `docker compose down -v` (this deletes data) so the script runs on a fresh boot.
