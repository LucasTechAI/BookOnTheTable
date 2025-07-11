from api.services.stats_service import get_overview_stats, get_category_stats
from src.api.utils.jwt_handler import get_current_user 
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/api/v1/stats", tags=["Stats"])

@router.get("/overview")
def overview(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Get overview statistics for the application.
    This endpoint returns general statistics such as total users, posts, and comments.
    Args:
        current_user (dict): The current user, obtained from the JWT token.
    Returns:
        dict: A dictionary containing the overview statistics.
    """
    overview_stats = get_overview_stats()
    return overview_stats


@router.get("/categories")
def categories(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Get statistics for categories.
    This endpoint returns statistics related to categories, such as the number of posts in each category.
    Args:
        current_user (dict): The current user, obtained from the JWT token.
    Returns:
        dict: A dictionary containing the category statistics.
    """
    categories_stats = get_category_stats()
    return categories_stats
