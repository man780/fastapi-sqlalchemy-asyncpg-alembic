from fastapi import APIRouter
from app.utils import get_logger

router = APIRouter(prefix="/system", tags=["System"])

logger = get_logger(__name__)


@router.get("/health_check")
def healt_check():
    """Health check"""
    return {"success": True}
