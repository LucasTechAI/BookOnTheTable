from pydantic import BaseModel
from typing import List


class CategoryResponse(BaseModel):
    category: str

    class Config:
        json_schema_extra = {"example": {"category": "Fiction"}}


class Categories:
    docs = {
        "summary": "All book categories",
        "response_model": List[CategoryResponse],
        "responses": {
            200: {
                "description": "List of all book categories.",
                "content": {
                    "application/json": {
                        "example": [
                            {"category": "Fiction"},
                            {"category": "Non-Fiction"},
                            {"category": "Science"},
                            {"category": "History"},
                        ]
                    }
                },
            },
            404: {
                "description": "No categories found.",
                "content": {
                    "application/json": {
                        "example": {"detail": "No matching books found"}
                    }
                },
            },
        },
    }
