from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api/health", tags=["Health"])


@router.get("")
def health_check():
    """Memeriksa status backend."""
    return {
        "status": "ok",
        "service": "WasteWise AI Backend",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
