from utils.database_manager import DatabaseManager
from src.api.utils.cache import cache_with_stats
from logging import getLogger, basicConfig, INFO
from pathlib import Path

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DB_PATH = Path(__file__).resolve().parents[3] / "tmp" / "bookonthetable.db"
manager = DatabaseManager(str(DB_PATH))

logger = getLogger(__name__)
basicConfig(level=INFO, format=FORMAT)


def get_overview_stats() -> dict:
    """
    Retrieve overview statistics for the book collection.

    Returns:
        dict: A dictionary containing:
            - total_books: Total number of books in the database.
            - average_price: Average price of all books.
            - ratings_distribution: A dictionary with ratings as keys and their counts as values.
    """
    try:
        logger.info("Retrieving overview statistics from the database.")
        total_books = manager.select("SELECT COUNT(*) as total FROM books")[0]["total"]
        avg_price = (
            manager.select("SELECT AVG(price) as avg_price FROM books")[0]["avg_price"]
            or 0.0
        )
        ratings = manager.select(
            """
            SELECT rating, COUNT(*) as count FROM books GROUP BY rating ORDER BY rating
        """
        )
        ratings_distribution = {str(row["rating"]): row["count"] for row in ratings}
        logger.info(
            f"Overview stats - Total Books: {total_books}, Average Price: {avg_price}, Ratings Distribution: {ratings_distribution}"
        )
        return {
            "total_books": total_books,
            "average_price": avg_price,
            "ratings_distribution": ratings_distribution,
        }
    except Exception as e:
        logger.error(f"Error retrieving overview statistics: {e}")
        return None


@cache_with_stats
def get_category_stats() -> dict:
    """
    Retrieve detailed statistics by category.

    Returns:
        dict: A dictionary with a list of categories, each containing:
            - name: The category name.
            - total_books: Number of books in the category.
            - average_price: Average price of books in the category.
    """
    try:
        logger.info("Retrieving category statistics from the database.")
        categories = manager.select(
            """
            SELECT category, COUNT(*) as total_books, AVG(price) as average_price
            FROM books
            GROUP BY category
            ORDER BY category
        """
        )
        categories = {
            "categories": [
                {
                    "name": row["category"],
                    "total_books": row["total_books"],
                    "average_price": row["average_price"] or 0.0,
                }
                for row in categories
            ]
        }
        logger.info(f"Retrieved category statistics: {categories}")
        return categories
    except Exception as e:
        logger.error(f"Error retrieving category statistics: {e}")
        return None
