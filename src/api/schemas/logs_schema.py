from typing import Optional, List
from pydantic import BaseModel


class LogResponse(BaseModel):
    """
    Schema representing a single log entry.
    """

    id: int
    timestamp: str
    method: str
    endpoint: str
    status_code: int
    response_time_ms: float
    user_agent: str
    ip_address: str
    username: Optional[str] = None
    query_params: str
    request_body: str


class Logs:
    """
    Documentation for the logs endpoint.
    """

    docs = {
        "summary": "List logs (requires auth)",
        "response_model": List[LogResponse],
        "responses": {
            200: {
                "description": "List of logs.",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": 1,
                                "timestamp": "2023-10-01T12:00:00Z",
                                "method": "GET",
                                "endpoint": "/api/v1/books",
                                "status_code": 200,
                                "response_time_ms": 150.5,
                                "user_agent": "Mozilla/5.0",
                                "ip_address": "...",
                                "username": "john_doe",
                                "query_params": "search=python",
                                "request_body": "{}",
                            }
                        ]
                    }
                },
            },
            404: {
                "description": "No logs found.",
                "content": {
                    "application/json": {"example": {"detail": "No logs found"}}
                },
            },
        },
    }


class LogDelete:
    """
    Documentation for the delete logs endpoint.
    """

    docs = {
        "summary": "Delete all logs (requires auth)",
        "description": "This endpoint deletes all logs from the system. Use with caution.",
        "response_model": dict,
        "responses": {
            200: {
                "description": "Logs deleted successfully.",
                "content": {
                    "application/json": {
                        "example": {"message": "All logs have been deleted."}
                    }
                },
            },
            403: {
                "description": "Forbidden. User does not have permission to delete logs.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "You do not have permission to perform this action."
                        }
                    }
                },
            },
        },
    }
