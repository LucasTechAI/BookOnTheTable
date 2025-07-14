from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List

from api.services.book_service import (
    get_all_books,
    get_book_by_id,
    search_books,
    get_top_rated_books,
    get_price_range_books,
)
from src.api.utils.jwt_handler import get_current_user
from api.schemas.books_schema import (
    Books,
    Search,
    TopRated,
    PriceRange,
    SearchById,
    BookResponse,
)

router = APIRouter(prefix="/api/v1/books", tags=["Books"])


@router.get("/", **Books.docs)
def list_books(current_user: dict = Depends(get_current_user)) -> List[BookResponse]:
    """
    Retrieve a list of all books in the database.
    Args:
        current_user (dict): The current authenticated user.
    Returns:
        list: A list of dictionaries, each representing a book.
    """
    books = get_all_books()
    if not books:
        raise HTTPException(status_code=404, detail="No matching books found")
    return [BookResponse(**book) for book in books]


@router.get("/search", **Search.docs)
def search(
    title: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
) -> List[BookResponse]:
    """
    Search for books by title and/or category.
    Args:
        title (Optional[str]): The title or part of the title to search for.
        category (Optional[str]): The category to filter books by.
        current_user (dict): The current authenticated user.
    Returns:
        list: A list of dictionaries representing the books that match the search criteria.
    Raises:
        HTTPException: If no matching books are found.
    """
    results = search_books(title, category)
    if not results:
        raise HTTPException(status_code=404, detail="No matching books found")
    return [BookResponse(**book) for book in results]


@router.get("/top-rated", **TopRated.docs)
def top_rated(
    limit: int = Query(
        10, gt=0, le=100, description="Maximum number of books to return"
    ),
    current_user: dict = Depends(get_current_user),
) -> List[BookResponse]:
    """
    Retrieve a list of top-rated books.
    Args:
        current_user (dict): The current authenticated user.
    Returns:
        list: A list of dictionaries representing the top-rated books.
    Raises:
        HTTPException: If no top-rated books are found.
    """
    top_rated_books = get_top_rated_books(limit)
    return [BookResponse(**book) for book in top_rated_books]


@router.get("/price-range", **PriceRange.docs)
def get_books_by_price_range(
    min_price: float = Query(0.0, ge=0.0),
    max_price: float = Query(1e9, ge=0.0),
    current_user: dict = Depends(get_current_user),
) -> List[BookResponse]:
    """
    Retrieve books within a specified price range.
    Args:
        min_price (float): The minimum price of the books to retrieve.
        max_price (float): The maximum price of the books to retrieve.
        current_user (dict): The current authenticated user.
    Returns:

    """
    books_in_price_range = get_price_range_books(min_price, max_price)
    return [BookResponse(**book) for book in books_in_price_range]


@router.get("/{book_id}", **SearchById.docs)
def book_id(
    book_id: int, current_user: dict = Depends(get_current_user)
) -> BookResponse:
    """
    Retrieve a specific book by its ID.
    Args:
        book_id (int): The ID of the book to retrieve.
        current_user (dict): The current authenticated user.
    Returns:
        BookResponse: A dictionary representing the book with the specified ID.
    Raises:
        HTTPException: If the book with the specified ID is not found.
    """
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse(**book)
