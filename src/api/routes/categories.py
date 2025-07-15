from src.api.services.category_service import get_all_categories
from src.api.utils.jwt_handler import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from src.api.schemas.categories_schema import CategoryResponse, Categories

router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])


@router.get("/", **Categories.docs)
def list_categories(current_user: dict = Depends(get_current_user)) -> CategoryResponse:
    """
    Retrieve a list of all book categories.
    Returns:
        list: A list of dictionaries, each representing a book category.
    """
    categories = get_all_categories()
    if not categories:
        raise HTTPException(status_code=404, detail="No matching books found")
    return [CategoryResponse(category=category["category"]) for category in categories]
