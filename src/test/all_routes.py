from pathlib import Path
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(ROOT_DIR)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
from utils.handler_api import APIHandler, logger
from random import randint

def assert_successful(response: tuple) -> None:
    """
    Asserts that the API response is successful and returns a boolean.
    Args:
        response (tuple): The response tuple from the API call.
    """
    json_data, status, payload = response
    if not status:
        logger.error(f"Request failed. Payload sent: {payload}, Response: {json_data}")
    if not (isinstance(json_data, (dict, list)) or json_data is None):
        logger.error(f"Unexpected response format: {json_data}")
    logger.info("Request successful.")

def main() -> None:
    BASE_URL = "https://book-on-the-table.vercel.app"
    api = APIHandler(BASE_URL)

    logger.info("Testing home endpoint...")
    assert_successful(api.test_home())

    logger.info("Registering a user for tests...")
    username, password = api.register_user()
    if not username:
        logger.error("User registration failed. Aborting tests.")
        return

    tokens, ok, _ = api.login_user(username, password)
    if not ok:
        logger.error("User login failed. Aborting tests.")
        return

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    logger.info("Testing protected endpoint...")
    assert_successful(api.test_protected(access_token))

    logger.info("Testing health check endpoint...")
    assert_successful(api.test_health(access_token))

    logger.info("Testing all books endpoint...")
    assert_successful(api.test_books_all(access_token))

    retry = randint(1, 3)
    for i in range(retry):
        logger.info(f"Testing book search endpoint - iteration {i+1}...")
        assert_successful(api.test_books_search(access_token))

        logger.info(f"Testing top-rated books endpoint - iteration {i+1}...")
        assert_successful(api.test_books_top(access_token))

        logger.info(f"Testing books price range endpoint - iteration {i+1}...")
        assert_successful(api.test_books_price_range(access_token))

        logger.info(f"Testing book by ID endpoint - iteration {i+1}...")
        assert_successful(api.test_book_by_id(access_token))

    logger.info("Testing categories endpoint...")
    assert_successful(api.test_categories(access_token))

    logger.info("Testing stats overview endpoint...")
    assert_successful(api.test_stats_overview(access_token))

    logger.info("Testing stats by categories endpoint...")
    assert_successful(api.test_stats_categories(access_token))

    logger.info("Testing ML features endpoint...")
    assert_successful(api.test_ml_features(access_token))

    for i in range(retry):
        logger.info(f"Testing ML training data endpoint - iteration {i+1}...")
        assert_successful(api.test_ml_training_data(access_token))

        logger.info(f"Testing ML predictions endpoint - iteration {i+1}...")
        assert_successful(api.test_ml_predictions(access_token))

    logger.info("Testing logs list endpoint...")
    assert_successful(api.test_logs_list(access_token))

    logger.info("Testing logs delete endpoint...")
    assert_successful(api.test_logs_delete(access_token))

    logger.info("Testing token refresh endpoint...")
    assert_successful(api.test_refresh(refresh_token))

    logger.info("All API tests completed successfully.")


if __name__ == "__main__":
    main()