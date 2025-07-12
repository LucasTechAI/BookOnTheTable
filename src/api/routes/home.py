from fastapi import APIRouter

router = APIRouter(tags=["Home"])

@router.get("/")
def read_root() -> dict:
    """
    Root endpoint for the BookOnTheTable API.
    Returns:
        dict: A welcome message for the API.
    """
    return {"message": "Welcome to the BookOnTheTable API 🚀"}
