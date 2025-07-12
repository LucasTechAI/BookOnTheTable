from fastapi import APIRouter, HTTPException, Query, status, Depends
from typing import List
from api.services.log_service import get_all_logs, delete_all_logs
from api.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/api/v1/logs", tags=["Logs"])

@router.get("/", summary="List logs (requires auth)")
def list_logs(limit: int = Query(100, ge=1, le=1000), user: dict = Depends(get_current_user)):
    logs = get_all_logs(limit)
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found")
    return logs

@router.delete("/", summary="Delete all logs (requires auth)")
def clear_logs(user: dict = Depends(get_current_user)):
    message = delete_all_logs()
    return {"message": message}
