from utils.database_manager import DatabaseManager
from src.api.utils.cache import cache_with_default
from logging import getLogger, basicConfig, INFO
from pathlib import Path

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DB_PATH = Path(__file__).resolve().parents[3] / "tmp" / "bookonthetable.db"
manager = DatabaseManager(str(DB_PATH))

logger = getLogger(__name__)
basicConfig(level=INFO, format=FORMAT)


@cache_with_default
def get_all_categories() -> list[dict]:
    """
    Retrieve all unique book categories from the database.
    Returns:
        list: A list of dictionaries, each containing a unique book category.
        If an error occurs, returns an empty list.
    """
    try:
        logger.info("Fetching all unique book categories from the database.")
        categories = manager.select(
            "SELECT DISTINCT category FROM books ORDER BY category"
        )
        return categories
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return []
