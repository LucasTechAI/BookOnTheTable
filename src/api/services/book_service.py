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
def get_all_books() -> list:
    """
    Retrieve all books from the database.
    Returns:
        list: A list of dictionaries, each representing a book.
        If an error occurs, returns an empty list.
    """
    try:
        logger.info("Fetching all books from the database.")
        books = manager.select("SELECT * FROM books")
        books = [dict(row) for row in books]
        return books
    except Exception as e:
        logger.error(f"Error fetching books: {e}")
        return []


@cache_with_default
def get_book_by_id(book_id: int) -> list:
    """
    Retrieve a specific book by its ID.
    Args:
        book_id (int): The ID of the book to retrieve.
    Returns:
        list: A list containing a single dictionary representing the book if found, otherwise an empty list.
    """
    try:
        logger.info(f"Fetching book with ID {book_id} from the database.")
        rows = manager.select("SELECT * FROM books WHERE id = ? LIMIT 1", (book_id,))
        book = [dict(row) for row in rows]
        return book
    except Exception as e:
        logger.error(f"Error fetching book with ID {book_id}: {e}")
        return []


@cache_with_default
def search_books(title: str = None, category: str = None) -> list:
    """
    Search for books by title and/or category.
    Args:
        title (str, optional): The title or part of the title to search for.
        category (str, optional): The category to filter books by.
    Returns:
        list: A list of dictionaries representing the books that match the search criteria.
    """
    try:
        logger.info(
            f"Searching for books with title '{title}' and category '{category}'."
        )
        query = "SELECT * FROM books WHERE 1=1"
        params = []

        if title:
            query += " AND LOWER(title) LIKE ?"
            params.append(f"%{title.lower()}%")

        if category:
            query += " AND LOWER(category) = ?"
            params.append(category.lower())
        results = manager.select(query, tuple(params))
        results = [dict(row) for row in results]
        return results
    except Exception as e:
        logger.error(f"Error searching for books: {e}")
        return []


@cache_with_default
def get_top_rated_books(limit: int = 10) -> list:
    """
    Retrieve the top-rated books from the database.
    Args:
        limit (int): The maximum number of top-rated books to retrieve. Default is 10.
    Returns:
        list: A list of dictionaries representing the top-rated books.
    """
    try:
        logger.info(f"Fetching top {limit} rated books from the database.")
        query = """
            SELECT * FROM books
            ORDER BY rating DESC, title ASC
            LIMIT ?
        """
        top_books = manager.select(query, (limit,))
        top_books = [dict(row) for row in top_books]
        return top_books
    except Exception as e:
        logger.error(f"Error fetching top-rated books: {e}")
        return []


@cache_with_default
def get_price_range_books(min_price: float = 0.0, max_price: float = 0.0) -> list:
    """
    Retrieve books within a specified price range.
    Args:
        min_price (float): The minimum price of the books to retrieve. Default is 0.0.
        max_price (float): The maximum price of the books to retrieve. Default is infinity.
    Returns:
        list: A list of dictionaries representing the books within the specified price range.
    """
    try:
        logger.info(f"Fetching books with price between {min_price} and {max_price}.")
        query = """
            SELECT * FROM books
            WHERE price BETWEEN ? AND ?
            ORDER BY price ASC
        """
        books = manager.select(query, (min_price, max_price))
        books = [dict(row) for row in books]
        return books
    except Exception as e:
        logger.error(f"Error fetching books by price range: {e}")
        return []
