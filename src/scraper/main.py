from logging import basicConfig, getLogger, INFO
from pandas import DataFrame, to_csv
from pathlib import Path
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(ROOT_DIR)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "tmp" / "bookonthetable.db"

from utils.database_manager import DatabaseManager
from scraping import BooksScraper


basicConfig(level=INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = getLogger(__name__)

manager = DatabaseManager(str(DB_PATH))


def _summary(books) -> None:
    """
    Prints a summary of the scraped books, including total categories and books per category.
    Args:
        books (list): List of dictionaries containing book data.
    Returns:
        None
    """
    if not books:
        logger.warning("No books found to summarize.")
        return

    from collections import Counter

    category_counts = Counter(book["category"] for book in books)
    total_categories = len(category_counts)

    logger.info(f"Total categories found: {total_categories}")

    print("\nSummary of Scraped Books")
    print(f"Total categories: {total_categories}")
    print("Books per category:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"- {cat}: {count} book(s)")


def _save_books_to_db(books: list) -> None:
    """
    Inserts all scraped books into the database in a single batch.

    Args:
        books (list): List of dictionaries containing book data.
    Returns:
        None
    """
    if not books:
        logger.warning("No books to save to the database.")
        return

    query = """
        INSERT INTO books (
            title, price, rating, availability, category,
            description, image_url, book_url, page_number, scraped_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    values_list = [
        (
            book["title"],
            book["price"],
            book["rating"],
            book["availability"],
            book["category"],
            book["description"],
            book["image_url"],
            book["book_url"],
            book["page_number"],
            book["scraped_at"],
        )
        for book in books
    ]
    try:
        inserted = manager.insert_many(query, values_list)
        logger.info(f"Successfully inserted {inserted} book(s) into the database.")
    except Exception as e:
        logger.error(f"Failed to insert books into the database: {e}")


def main():
    scraper = BooksScraper()

    try:
        books = scraper.scrape_all_books()
        _save_books_to_db(books)
        books = DataFrame(books)
        books.to_csv(BASE_DIR / "data" / "books_data.csv", index=False)

        _summary(books)
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}")


if __name__ == "__main__":
    main()
