from fastapi import FastAPI

from app.routes import router


def create_app() -> FastAPI:
    application = FastAPI(
        title="AI Ecosystem API",
        version="0.1.0",
    )
    application.include_router(router)
    return application
