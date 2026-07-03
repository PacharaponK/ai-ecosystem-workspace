# AI Ecosystem Workspace

Workspace for the 241-353 AI Ecosystem project.

## Structure

- `compose.yml` — Docker Compose setup for a Redis instance used by the project.
- `diagrams/` — Architecture diagrams (`overview.drawio`, `overview.png`).
- `work-result/` — Screenshots/results captured during development.

## Getting Started

Start the Redis service:

```bash
docker compose up -d
```

Redis will be available on `localhost:6379`.
