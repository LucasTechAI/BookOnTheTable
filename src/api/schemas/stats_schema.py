from pydantic import BaseModel
from typing import Dict, List


class OverviewResponse(BaseModel):
    """
    Schema representing general statistics for the book collection.
    """

    total_books: int
    average_price: float
    ratings_distribution: Dict[str, int]

    class Config:
        title = "StatsResponse"
        schema_extra = {
            "example": {
                "total_books": 123,
                "average_price": 45.67,
                "ratings_distribution": {"1": 10, "2": 20, "3": 30, "4": 40, "5": 23},
            }
        }


class Overview:
    """
    OpenAPI documentation for the statistics endpoint.
    """

    docs = {
        "summary": "Statistics endpoint",
        "response_model": OverviewResponse,
        "responses": {
            200: {
                "description": "Statistics retrieved successfully.",
                "content": {
                    "application/json": {
                        "example": {
                            "total_books": 123,
                            "average_price": 45.67,
                            "ratings_distribution": {
                                "1": 10,
                                "2": 20,
                                "3": 30,
                                "4": 40,
                                "5": 23,
                            },
                        }
                    }
                },
            },
            503: {
                "description": "Service is not healthy.",
                "content": {
                    "application/json": {"example": {"detail": "Service is down"}}
                },
            },
            404: {
                "description": "No matching books found",
                "content": {
                    "application/json": {
                        "example": {"detail": "No matching books found"}
                    }
                },
            },
        },
    }


class CategoryStats(BaseModel):
    """
    Schema representing statistics for a single category.
    """

    name: str
    total_books: int
    average_price: float

    class Config:
        schema_extra = {
            "example": {"name": "Fiction", "total_books": 50, "average_price": 36.07}
        }


class CategoriesResponse(BaseModel):
    """
    Schema representing the response for categories statistics.
    """

    categories: List[CategoryStats]

    class Config:
        schema_extra = {
            "example": {
                "categories": [
                    {"name": "Fiction", "total_books": 12, "average_price": 34.56},
                    {"name": "Non-Fiction", "total_books": 78, "average_price": 90.12},
                ]
            }
        }


class Categories:
    """
    OpenAPI documentation for the categories statistics endpoint.
    """

    docs = {
        "summary": "Categories statistics endpoint",
        "response_model": CategoriesResponse,
        "responses": {
            200: {
                "description": "Categories statistics retrieved successfully.",
                "content": {
                    "application/json": {
                        "example": {
                            "categories": [
                                {
                                    "name": "Fiction",
                                    "total_books": 12,
                                    "average_price": 34.56,
                                },
                                {
                                    "name": "Non-Fiction",
                                    "total_books": 78,
                                    "average_price": 90.12,
                                },
                            ]
                        }
                    }
                },
            },
            503: {
                "description": "Service is not healthy.",
                "content": {
                    "application/json": {"example": {"detail": "Service is down"}}
                },
            },
            404: {
                "description": "No matching books found",
                "content": {
                    "application/json": {
                        "example": {"detail": "No matching books found"}
                    }
                },
            },
        },
    }
