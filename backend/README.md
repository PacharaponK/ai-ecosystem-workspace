# AI Ecosystem Backend

Install/sync dependencies and start the FastAPI development server:

```powershell
uv sync
uv run python main.py
```

The API is available at `http://localhost:8000`, with interactive docs at
`http://localhost:8000/docs`.

Application setup lives in `app/application.py`, while HTTP routes live in
`app/routes.py`. Add new route modules under `app/` and register their routers
in the application factory as the API grows.

Run the basic in-process sandbox check:

```powershell
uv run python sandbox/test_fastapi.py
```
