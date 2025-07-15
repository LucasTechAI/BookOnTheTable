from src.api.services.log_service import get_all_logs, delete_all_logs
from fastapi import APIRouter, HTTPException, Query, Depends
from src.api.utils.jwt_handler import get_current_user
from src.api.schemas.logs_schema import LogResponse, Logs, LogDelete
from typing import List

router = APIRouter(prefix="/api/v1/logs", tags=["Logs"])


@router.get("/", **Logs.docs)
def list_logs(
    limit: int = Query(100, ge=1, le=1000), user: dict = Depends(get_current_user)
) -> List[LogResponse]:
    """
    Retrieve a list of logs with an optional limit.
    Args:
        limit (int): The maximum number of logs to return (default is 100).
        user (dict): The current authenticated user.
    Returns:
        List[LogResponse]: A list of log entries.
    Raises:
        HTTPException: If no logs are found or if the limit is invalid.
    """
    logs = get_all_logs(limit)
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found")
    return [LogResponse(**log) for log in logs]


@router.delete("/", **LogDelete.docs)
def clear_logs(user: dict = Depends(get_current_user)) -> dict:
    """
    Clear all logs from the system.
    Args:
        user (dict): The current authenticated user.
    Returns:
        dict: A message indicating the result of the operation.
    """
    message = delete_all_logs()
    return {"message": message}
