from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class BookResponse(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    availability: str
    category: str
    description: Optional[str] = None
    image_url: HttpUrl
    book_url: HttpUrl
    page_number: Optional[int]
    scraped_at: datetime

    class Config:
        title = "BookResponse"
        schema_extra = {
            "example": {
                "id": 1,
                "title": "It's Only the Himalayas",
                "price": 45.17,
                "rating": 2,
                "availability": "In stock",
                "category": "Travel",
                "description": "...",
                "image_url": "...",
                "book_url": "...",
                "page_number": 1,
                "scraped_at": "...",
            }
        }


class Books:
    docs = {
        "summary": "All books",
        "response_model": List[BookResponse],
        "responses": {
            200: {
                "description": "Books matching the search criteria.",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": 1,
                                "title": "It's Only the Himalayas",
                                "price": 45.17,
                                "rating": 2,
                                "availability": "In stock",
                                "category": "Travel",
                                "description": "...",
                                "image_url": "...",
                                "book_url": "...",
                                "page_number": 1,
                                "scraped_at": "...",
                            }
                        ]
                    }
                },
            },
            404: {
                "description": "No books found matching the given title and/or category.",
                "content": {
                    "application/json": {
                        "example": {"detail": "No matching books found"}
                    }
                },
            },
        },
    }


class Search:
    docs = {
        "summary": "Search books by title and/or category",
        "response_model": List[BookResponse],
        "responses": {
            200: {
                "description": "Books matching the search criteria.",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": 1,
                                "title": "It's Only the Himalayas",
                                "price": 45.17,
                                "rating": 2,
                                "availability": "In stock",
                                "category": "Travel",
                                "description": "...",
                                "image_url": "...",
                                "book_url": "...",
                                "page_number": 1,
                                "scraped_at": "...",
                            }
                        ]
                    }
                },
            },
            404: {
                "description": "No books found matching the given title and/or category.",
                "content": {
                    "application/json": {
                        "example": {"detail": "No matching books found"}
                    }
                },
            },
        },
    }


class TopRated:
    docs = {
        "summary": "Get top-rated books",
        "response_model": List[BookResponse],
        "responses": {
            200: {
                "description": "Top-rated books retrieved successfully.",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": 895,
                                "title": '"Most Blessed of the Patriarchs": Thomas Jefferson and the Empire of the Imagination',
                                "price": 44.48,
                                "rating": 5,
                                "availability": "In stock",
                                "category": "History",
                                "description": "...",
                                "image_url": "...",
                                "book_url": "...",
                                "page_number": 1,
                                "scraped_at": "...",
                            }
                        ]
                    }
                },
            },
            401: {
                "description": "Unauthorized access.",
                "content": {
                    "application/json": {
                        "example": {"detail": "Invalid authentication credentials"}
                    }
                },
            },
        },
    }


class PriceRange:
    docs = {
        "summary": "Get books within a price range",
        "response_model": List[BookResponse],
        "responses": {
            200: {
                "description": "Books within the specified price range.",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": 1,
                                "title": "It's Only the Himalayas",
                                "price": 45.17,
                                "rating": 2,
                                "availability": "In stock",
                                "category": "Travel",
                                "description": "...",
                                "image_url": "...",
                                "book_url": "...",
                                "page_number": 1,
                                "scraped_at": "...",
                            }
                        ]
                    }
                },
            },
            404: {
                "description": "No books found within the specified price range.",
                "content": {
                    "application/json": {
                        "example": {"detail": "No matching books found"}
                    }
                },
            },
        },
    }


class SearchById:
    docs = {
        "summary": "Get book by ID",
        "response_model": BookResponse,
        "responses": {
            200: {
                "description": "Book retrieved successfully.",
                "content": {
                    "application/json": {
                        "example": {
                            "id": 1,
                            "title": "It's Only the Himalayas",
                            "price": 45.17,
                            "rating": 2,
                            "availability": "In stock",
                            "category": "Travel",
                            "description": "...",
                            "image_url": "...",
                            "book_url": "...",
                            "page_number": 1,
                            "scraped_at": "...",
                        }
                    }
                },
            },
            404: {
                "description": "Book not found.",
                "content": {
                    "application/json": {"example": {"detail": "Book not found"}}
                },
            },
        },
    }
