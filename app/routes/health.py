from fastapi import APIRouter
from app.config import settings

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}
