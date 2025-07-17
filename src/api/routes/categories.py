from src.api.schemas.categories_schema import CategoryResponse, Categories
from src.api.services.category_service import get_all_categories
from src.api.utils.jwt_handler import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from logging import getLogger, basicConfig, INFO

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])
logger = getLogger(__name__)
basicConfig(level=INFO, format=FORMAT)

@router.get("/", **Categories.docs)
def list_categories(current_user: dict = Depends(get_current_user)) -> CategoryResponse:
    """
    Retrieve a list of all book categories.
    Returns:
        list: A list of dictionaries, each representing a book category.
    """
    try:
        logger.info("Fetching all book categories.")
        categories = get_all_categories()
        if not categories:
            raise HTTPException(status_code=404, detail="No matching books found")
        return [CategoryResponse(category=category["category"]) for category in categories]  
    except Exception as e:
        logger.error(f"Categories {categories}, type: {type(categories)}")
        logger.error(f"Error fetching categories: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
