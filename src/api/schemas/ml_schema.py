from typing import List
from pydantic import BaseModel


class FeatureItem(BaseModel):
    """
    Schema representing a single ML feature entry.
    """
    id: int
    price: float
    rating: int
    category: str
    availability: str


class FeatureResponse(BaseModel):
    """
    Schema representing a list of ML features.
    """
    features: List[FeatureItem]


class Features:
    """
    Documentation for the ML features endpoint.
    """
    docs = {
        "summary": "Get ML-ready features",
        "response_model": FeatureResponse,
        "responses": {
            200: {
                "description": "List of ML features.",
                "content": {
                    "application/json": {
                        "example": {
                            "features": [
                                {
                                    "id": 1,
                                    "price": 45.17,
                                    "rating": 2,
                                    "category": "Travel",
                                    "availability": "In stock"
                                }
                            ]
                        }
                    }
                },
            },
            404: {
                "description": "No features found.",
                "content": {
                    "application/json": {"example": {"detail": "No features found"}}
                },
            },
        },
    }


class TrainingItem(BaseModel):
    """
    Schema representing a single training data entry.
    """
    features: List[float]
    label: int


class TrainingDataResponse(BaseModel):
    """
    Schema representing a list of training data entries.
    """
    training_data: List[TrainingItem]


class TrainingData:
    """
    Documentation for the ML training data endpoint.
    """
    docs = {
        "summary": "Get ML training dataset",
        "response_model": TrainingDataResponse,
        "responses": {
            200: {
                "description": "List of training data.",
                "content": {
                    "application/json": {
                        "example": {
                            "training_data": [
                                {"features": [45.17, 2], "label": 0}
                            ]
                        }
                    }
                },
            },
            404: {
                "description": "No training data found.",
                "content": {
                    "application/json": {"example": {"detail": "No training data found"}}
                },
            },
        },
    }


class PredictionFeature(BaseModel):
    """
    Schema representing a single feature for ML prediction.
    """
    price: float
    category: str

class PredictionRequest(BaseModel):
    """
    Schema for ML prediction request.
    """
    features: List[PredictionFeature]


class PredictionResponse(BaseModel):
    """
    Schema for ML prediction response.
    """
    predictions: List[int]


class Predictions:
    """
    Documentation for the ML predictions endpoint.
    """
    docs = {
        "summary": "Submit data for ML predictions",
        "response_model": PredictionResponse,
        "responses": {
            200: {
                "description": "Predictions returned successfully.",
                "content": {
                    "application/json": {
                        "example": {
                            "predictions": [0, 1]
                        }
                    }
                },
            },
            400: {
                "description": "Invalid input data.",
                "content": {
                    "application/json": {"example": {"detail": "Invalid features format"}}
                },
            },
        },
    }