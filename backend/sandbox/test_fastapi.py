"""Basic in-process checks for the FastAPI application."""
import asyncio
import sys
from pathlib import Path

from httpx import ASGITransport, AsyncClient

# Add backend/ to the import path when this file is run directly.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import create_app


async def main() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        root_response = await client.get("/")
        assert root_response.status_code == 200
        assert root_response.json() == {"message": "AI Ecosystem API"}

        health_response = await client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json() == {"status": "ok"}

    print("[OK] FastAPI root and health endpoints passed")


if __name__ == "__main__":
    asyncio.run(main())
