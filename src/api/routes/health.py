from src.api.utils.jwt_handler import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from api.services.health_service import check_health

router = APIRouter(prefix="/api/v1/health", tags=["Health"])

@router.get("/", summary="API health check")
def health(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Health check endpoint to verify if the API is running.
    Returns:
        dict: A dictionary indicating the health status of the API.
    """
    health = check_health()
    if not health:
        raise HTTPException(status_code=404, detail="No matching books found")
    return health
