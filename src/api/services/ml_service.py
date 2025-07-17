from src.api.utils.cache import cache_with_ml_features, cache_with_ml_training_data, cache_with_predict
from src.api.services.book_service import get_all_books
from logging import getLogger, basicConfig, INFO

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logger = getLogger(__name__)
basicConfig(level=INFO, format=FORMAT)

@cache_with_ml_features
def extract_features() -> list:
    """
    Extracts features from books for ML processing.
    Returns:
        list: A list of dictionaries, each containing features for ML.
    """
    try:
        logger.info("Extracting features from books for ML processing.")
        books = get_all_books()
        books = [
            {
                "id": book.get("id", 0),
                "price": book.get("price", 0.0),
                "rating": book.get("rating", 0.0),
                "category": book.get("category", ""),
                "availability": book.get("availability", "In stock")
            }
            for book in books
        ]
        return books
    except Exception as e:
        logger.error(f"Error extracting features: {e}")
        return None


@cache_with_ml_training_data
def get_training_data() -> list:
    """
    Retrieves training data for ML processing.
    Returns:
        list: A list of dictionaries, each containing features and labels for ML.
    """
    try:
        logger.info("Retrieving training data for ML processing.")
        books = get_all_books()
        books = [
            {
                "features": [book.get("price", 0.0), book.get("rating", 0.0)],
                "label": 0 if book.get("rating", 0) < 4 else 1
            }
            for book in books
        ]
        return books
    except Exception as e:
        logger.error(f"Error retrieving training data: {e}")
        return None

@cache_with_predict
def predict(features: list) -> list:
    """
    Predicts labels based on features for ML processing.
    Args:
        features (list): A list of dicts with 'price' and 'category' for each item.
    Returns:
        list: A list of predicted labels (0 or 1).
    """
    try:
        logger.info("Predicting labels based on features for ML processing.")
        prediction = [
            1 if feat.price >= 30.0 or feat.category == "Travel"
            else 0 for feat in features
        ]
        return prediction
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return None