from pathlib import Path
import sys
import os
import random

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(ROOT_DIR)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

from utils.handler_api import APIHandler, logger

def assert_successful(response: tuple) -> None:
    """
    Checks if the API response is successful.
    """
    json_data, status, payload = response
    if not status:
        logger.error(f"Request failed.\nPayload: {payload}\nResponse: {json_data}")
    elif not isinstance(json_data, (dict, list)) and json_data is not None:
        logger.error(f"Unexpected response format: {json_data}")
    else:
        logger.info("Request successful.")

def main() -> None:
    BASE_URL = "https://book-on-the-table.vercel.app"
    api = APIHandler(BASE_URL)

    logger.info("Testing home endpoint...")
    assert_successful(api.test_home())

    logger.info("Registering test user...")
    username, password = api.register_user()
    if not username:
        logger.error("User registration failed. Aborting.")
        return

    tokens, ok, _ = api.login_user(username, password)
    if not ok:
        logger.error("Login failed. Aborting.")
        return

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    # Define a pool of test methods
    route_tests = [
        lambda: api.test_protected(access_token),
        lambda: api.test_health(access_token),
        lambda: api.test_books_all(access_token),
        lambda: api.test_books_search(access_token),
        lambda: api.test_books_top(access_token),
        lambda: api.test_books_price_range(access_token),
        lambda: api.test_book_by_id(access_token),
        lambda: api.test_categories(access_token),
        lambda: api.test_stats_overview(access_token),
        lambda: api.test_stats_categories(access_token),
        lambda: api.test_ml_features(access_token),
        lambda: api.test_ml_training_data(access_token),
        lambda: api.test_ml_predictions(access_token),
        lambda: api.test_logs_list(access_token),
        lambda: api.test_logs_delete(access_token),
        lambda: api.test_refresh(refresh_token),
    ]

    # Randomly select N routes to test
    num_routes_to_test = random.randint(5, len(route_tests))
    selected_tests = random.sample(route_tests, num_routes_to_test)

    logger.info(f"Randomly selected {num_routes_to_test} routes for testing...\n")

    for i, test_func in enumerate(selected_tests, start=1):
        logger.info(f"[{i}] Executing test: {test_func.__name__}")
        assert_successful(test_func())

    logger.info("Random route testing completed successfully.")

if __name__ == "__main__":
    main()
