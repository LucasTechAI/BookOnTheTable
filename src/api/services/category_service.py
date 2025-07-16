from utils.database_manager import DatabaseManager
from logging import getLogger, basicConfig, INFO
from pathlib import Path

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DB_PATH = Path(__file__).resolve().parents[3] / "tmp" / "bookonthetable.db"
manager = DatabaseManager(str(DB_PATH))

logger = getLogger(__name__)
basicConfig(level=INFO, format=FORMAT)

def get_all_categories() -> list[dict]:
    """
    Retrieve all unique book categories from the database.
    Applies normalization to avoid duplicates caused by case or extra spaces.
    Returns:
        list: A list of dictionaries, each containing a unique book category.
        If an error occurs, returns an empty list.
    """
    try:
        logger.info("Fetching all unique book categories from the database.")
        rows = manager.select("SELECT category FROM books")
        categories_raw = [row["category"].strip() for row in rows if row["category"]]

        unique_normalized = sorted(set(c.strip() for c in categories_raw))

        categories = [{"category": c} for c in unique_normalized]
        return categories
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return []
