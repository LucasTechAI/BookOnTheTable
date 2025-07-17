from src.api.services.ml_service import extract_features, get_training_data, predict
from fastapi import APIRouter, Depends, Body, HTTPException
from src.api.utils.jwt_handler import get_current_user
from logging import getLogger, basicConfig, INFO
from src.api.schemas.ml_schema import (
    Features,
    Predictions, 
    TrainingData,
    FeatureResponse,
    TrainingDataResponse,
    PredictionRequest,
    PredictionResponse,
)
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
router = APIRouter(prefix="/api/v1/ml", tags=["ML"])
logger = getLogger(__name__)
basicConfig(level=INFO, format=FORMAT)

@router.get("/features", **Features.docs)
def get_features(current_user: dict = Depends(get_current_user)) -> FeatureResponse:
    """
    Returns a list of ML-ready features extracted from books.
    Args:
        current_user (dict): The current authenticated user.
    Returns:
        FeatureResponse: A response containing the extracted features.
    """
    try:
        features = extract_features()
        return FeatureResponse(features=features)
    except Exception as e:
        logger.error(f"Error extracting features: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/training-data", **TrainingData.docs)
def get_training_data_endpoint(current_user: dict = Depends(get_current_user)) -> TrainingDataResponse:
    """
    Returns a dataset for ML model training.
    Args:
        current_user (dict): The current authenticated user.
    Returns:
        TrainingDataResponse: A response containing the training data.
    """
    try:
        training_data = get_training_data()
        return TrainingDataResponse(training_data=training_data)
    except Exception as e:
        logger.error(f"Error fetching training data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/predictions", **Predictions.docs)
def get_predictions(
        request: PredictionRequest = Body(...),
        current_user: dict = Depends(get_current_user)
    ) -> PredictionResponse:
    """
    Submits features for ML predictions and returns the predicted labels.
    Args:
        request (PredictionRequest): The request body containing features for prediction.
        current_user (dict): The current authenticated user.
    Returns:
        PredictionResponse: A response containing the predicted labels.
    """
    try:
        predictions = predict(request.features)
        return PredictionResponse(predictions=predictions)
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")