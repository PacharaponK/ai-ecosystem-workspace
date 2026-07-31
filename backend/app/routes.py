from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    return {"message": "AI Ecosystem API"}


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
