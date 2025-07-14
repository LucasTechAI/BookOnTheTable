from api.schemas.stats_schema import (
    Categories,
    CategoriesResponse,
    Overview,
    OverviewResponse,
)
from api.services.stats_service import get_overview_stats, get_category_stats
from src.api.utils.jwt_handler import get_current_user
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1/stats", tags=["Stats"])


@router.get("/overview", **Overview.docs)
def overview(current_user: dict = Depends(get_current_user)) -> OverviewResponse:
    """
    Get overview statistics for the application.
    This endpoint returns general statistics such as total users, posts, and comments.
    Args:
        current_user (dict): The current user, obtained from the JWT token.
    Returns:
        OverviewResponse: A response containing the overview statistics.
    """
    overview_stats = get_overview_stats()
    return OverviewResponse(**overview_stats)


@router.get("/categories", **Categories.docs)
def categories(current_user: dict = Depends(get_current_user)) -> CategoriesResponse:
    """
    Get statistics for categories.
    This endpoint returns statistics related to categories, such as the number of posts in each category.
    Args:
        current_user (dict): The current user, obtained from the JWT token.
    Returns:
        CategoriesResponse: A response containing the category statistics.
    """
    categories_stats = get_category_stats()
    return CategoriesResponse(**categories_stats)
