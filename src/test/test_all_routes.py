from random import choices, randint, uniform, choice
from requests import request, exceptions, Response
from logging import getLogger, basicConfig, INFO
import string

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
BASE_URL = "https://book-on-the-table.vercel.app"

logger = getLogger(__name__)
basicConfig(level=INFO, format=FORMAT)

CATEGORIES = [
    "Academic", "Add a comment", "Adult Fiction", "Art",
    "Autobiography", "Biography", "Business", "Childrens",
    "Christian", "Christian Fiction", "Classics", "Contemporary",
    "Crime", "Cultural", "Default", "Erotica",
    "Fantasy", "Fiction", "Food and Drink", "Health",
    "Historical", "Historical Fiction", "History", "Horror",
    "Humor", "Music", "Mystery", "New Adult",
    "Nonfiction", "Novels", "Paranormal", "Parenting",
    "Philosophy", "Poetry", "Politics", "Psychology",
    "Religion", "Romance", "Science", "Science Fiction",
    "Self Help", "Sequential Art", "Short Stories", "Spirituality",
    "Sports and Games", "Suspense", "Thriller", "Travel",
    "Womens Fiction", "Young Adult"
]

def random_string(length:int=8) -> str:
    """
    Generete a random string of lowercase letters with the specified length.
    Args:
        length (int): The length of the random string to generate.
    Returns:
        str: A random string of lowercase letters.
    """
    random_choices = choices(string.ascii_lowercase, k=length)
    random_choices = ''.join(random_choices)
    return random_choices


def send_request_with_log(method: str, url: str, **kwargs) -> Response | None:
    """
    Make a safe HTTP request and log the response.
    Args:
        method (str): The HTTP method to use (GET, POST, etc.).
        url (str): The URL to request.
        **kwargs: Additional arguments to pass to the request.
    Returns:
        requests.Response | None: The response object if successful, None otherwise.
    """
    try:
        response = request(method, url, timeout=10, **kwargs)
        response.raise_for_status()
        logger.info(f"[{method}] {url} - {response.status_code}")
        return response
    except exceptions.HTTPError as e:
        logger.error(f"[HTTPError] {url} - {e}")
    except exceptions.RequestException as e:
        logger.error(f"[RequestException] {url} - {e}")
    return None


def test_home() -> None:
    """
    Test the home route of the API.
    """
    send_request_with_log("GET", f"{BASE_URL}/")


def test_health(token: str) -> None:
    """
    Test the health check route of the API.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/health/",
        "headers": headers
    }
    send_request_with_log(**__args)
    

def register_user() -> tuple[str, str] | None:
    """
    Register a new user for testing purposes.
    Returns:
        tuple[str, str] | None: A tuple containing the username and password if successful,
        None otherwise.
    """
    username = f"user_{random_string()}"
    password = random_string()
    payload = {
        "username": username, 
        "password": password
    }
    __args = {
        "method": "POST",
        "url": f"{BASE_URL}/api/v1/auth/register",
        "json": payload
    }
    res = send_request_with_log(**__args)
    if res:
        return username, password
    return None, None

def login_user(username, password) -> dict | None:
    """
    Log in a user and return the access and refresh tokens.
    Args:
        username (str): The username of the user.
        password (str): The password of the user.
    Returns:
        dict | None: A dictionary containing the access and refresh tokens if successful,
        None otherwise.
    """
    payload = {
        "username": username, 
        "password": password
    }
    __args = {
        "method": "POST",
        "url": f"{BASE_URL}/api/v1/auth/login",
        "json": payload
    }
    res = send_request_with_log(**__args)
    if res:
        return res.json()
    return None

def test_protected(token: str) -> None:
    """
    Test a protected route that requires authentication.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/auth/protected",
        "headers": headers
    }
    send_request_with_log(**__args)
    

def test_refresh(refresh_token: str) -> None:
    """
    Test the refresh token endpoint to obtain a new access token.
    Args:
        refresh_token (str): The refresh token to use for obtaining a new access token.
    """
    payload = {"refresh_token": refresh_token}
    __args = {
        "method": "POST",
        "url": f"{BASE_URL}/api/v1/auth/refresh",
        "json": payload
    }
    send_request_with_log(**__args)
    

def test_books_all(token: str) -> None:
    """
    Test the route to get all books.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/books/",
        "headers": headers
    }
    send_request_with_log(**__args)
    

def test_books_search(token: str) -> None:
    """
    Test the route to search for books by title and category.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    category = choice(CATEGORIES)
    title = random_string(5) if randint(0, 1) else category
    params = {
        "title": title if randint(0, 1) else "", 
        "category": category if randint(0, 1) else ""
    }
    logger.info(f"Searching for books with title: '{params['title']}' and category: '{params['category']}'")
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/books/search",
        "headers": headers,
        "params": params
    }
    send_request_with_log(**__args)
    

def test_books_top(token:str) -> None:
    """
    Test the route to get top-rated books.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": randint(1, 20)}
    logger.info(f"Fetching top-rated books with limit: {params['limit']}")
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/books/top-rated",
        "headers": headers,
        "params": params
    }
    send_request_with_log(**__args)
    

def test_books_price_range(token:str) -> None:
    """
    Test the route to get books within a specified price range.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    min_price = randint(1, 20)
    max_price = min_price + randint(5, 30)
    params = {
        "min_price": min_price if randint(0, 1) else 0,
        "max_price": max_price if randint(0, 1) else 100
    }
    logger.info(f"Fetching books with price range: {params['min_price']} - {params['max_price']}")
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/books/price-range",
        "headers": headers,
        "params": params
    }
    send_request_with_log(**__args)
    

def test_book_by_id(token:str) -> None:
    """
    Test the route to get a book by its ID.
    Args:
        token (str): The access token for authentication.
    """
    book_id = randint(1, 1000)  
    headers = {"Authorization": f"Bearer {token}"}
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/books/{book_id}",
        "headers": headers
    }
    send_request_with_log(**__args)
    

def test_categories(token:str) -> None:
    """
    Test the route to get all book categories.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/categories/",
        "headers": headers
    }
    send_request_with_log(**__args)

def test_stats_overview(token:str) -> None:
    """
    Test the route to get an overview of statistics.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/stats/overview",
        "headers": headers
    }
    send_request_with_log(**__args)
    

def test_stats_categories(token:str) -> None:
    """
    Test the route to get statistics by categories.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/stats/categories",
        "headers": headers
    }
    send_request_with_log(**__args)
    

def test_ml_features(token:str) -> None:
    """
    Test the route to get ML-ready features extracted from books.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/ml/features",
        "headers": headers
    }
    send_request_with_log(**__args)
    

def test_ml_training_data(token:str) -> None:
    """
    Test the route to get training data for ML model training.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/ml/training-data",
        "headers": headers
    }
    send_request_with_log(**__args)
    

def test_ml_predictions(token:str) -> None:
    """
    Test the route to submit features for ML predictions.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "features": [
            {
                "price": round(uniform(5.0, 100.0), 2),
                "category": choice(CATEGORIES)
            }
        ]
    }
    __args = {
        "method": "POST",
        "url": f"{BASE_URL}/api/v1/ml/predictions",
        "headers": headers,
        "json": payload
    }
    send_request_with_log(**__args)
    

def test_logs_list(token:str) -> None:
    """
    Test the route to list logs.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    __args = {
        "method": "GET",
        "url": f"{BASE_URL}/api/v1/logs/",
        "headers": headers
    }
    send_request_with_log(**__args)
    

def test_logs_delete(token:str) -> None:
    """
    Test the route to delete logs.
    Args:
        token (str): The access token for authentication.
    """
    headers = {"Authorization": f"Bearer {token}"}
    __args = {
        "method": "DELETE",
        "url": f"{BASE_URL}/api/v1/logs/",
        "headers": headers
    }
    send_request_with_log(**__args)
    

def main() -> None:
    logger.info(" Starting API tests...")
    test_home()

    logger.info("Registering a new user for testing...")
    username, password = register_user()
    if not username:
        logger.error("Failed to register user.")
        return
    
    logger.info(f"Testing Login route with username: {username}")
    tokens = login_user(username, password)
    if not tokens:
        logger.error("Failed to log in user.")
        return

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    logger.info("Testing protected route with access token...")
    test_protected(access_token)

    logger.info("Testing health route...")
    test_health(access_token)


    logger.info("Testing book routes...")
    test_books_all(access_token)
    for i in range(randint(1, 5)):
        logger.info(f"Testing book routes iteration {i+1}")
        test_books_search(access_token)
        test_books_top(access_token)
        test_books_price_range(access_token)
        test_book_by_id(access_token)

    logger.info("Testing categories route...")
    test_categories(access_token)

    logger.info("Testing stats routes...")
    test_stats_overview(access_token)
    test_stats_categories(access_token)

    logger.info("Testing ML routes...")
    test_ml_features(access_token)
    for i in range(randint(1, 3)):
        logger.info(f"Testing ML routes iteration {i+1}")
        test_ml_training_data(access_token)
        test_ml_predictions(access_token)

    logger.info("Testing logs routes...")
    test_logs_list(access_token)
    test_logs_delete(access_token)
    
    logger.info("Testing refresh token route...")
    test_refresh(refresh_token)

    logger.info("All API tests completed successfully.")


if __name__ == "__main__":
    main()
