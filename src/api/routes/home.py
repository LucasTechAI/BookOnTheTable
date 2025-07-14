from fastapi import APIRouter

router = APIRouter(tags=["Home"])


@router.get(
    "/",
    summary="Root Endpoint",
    description="Root endpoint for the BookOnTheTable API",
    responses={
        200: {
            "description": "Welcome message",
            "content": {
                "application/json": {
                    "example": {"message": "Welcome to the BookOnTheTable API 🚀"}
                }
            },
        }
    },
)
def read_root() -> dict:
    """
    Root endpoint for the BookOnTheTable API.
    Returns:
        dict: A welcome message for the API.
    """
    return {"message": "Welcome to the BookOnTheTable API 🚀"}
