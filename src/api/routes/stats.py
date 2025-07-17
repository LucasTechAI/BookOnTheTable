from src.api.services.stats_service import get_overview_stats, get_category_stats
from src.api.utils.jwt_handler import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from logging import getLogger, basicConfig, INFO
from src.api.schemas.stats_schema import (
    Categories,
    CategoriesResponse,
    Overview,
    OverviewResponse,
)

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
router = APIRouter(prefix="/api/v1/stats", tags=["Stats"])
logger = getLogger(__name__)
basicConfig(level=INFO, format=FORMAT)

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
    try:
        overview_stats = get_overview_stats()
        return OverviewResponse(**overview_stats)
    except Exception as e:
        logger.error(f"Error fetching overview stats: {e}")
        logger.error(f"Overview Stats: {overview_stats}, type: {type(overview_stats)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


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
    try:
        categories_stats = get_category_stats()
        return CategoriesResponse(**categories_stats)
    except Exception as e:
        logger.error(f"Error fetching category stats: {e}")
        logger.error(f"Categories Stats: {categories_stats}, type: {type(categories_stats)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
