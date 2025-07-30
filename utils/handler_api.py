# handler_apis.py

from random import choices, randint, uniform, choice
from requests import request, exceptions, Response
from logging import getLogger, basicConfig, INFO
import string

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logger = getLogger(__name__)
basicConfig(level=INFO, format=FORMAT)

CATEGORIES = [  
    "Academic", "Add a comment", "Adult Fiction", "Art", "Autobiography", "Biography",
    "Business", "Childrens", "Christian", "Christian Fiction", "Classics", "Contemporary",
    "Crime", "Cultural", "Default", "Erotica", "Fantasy", "Fiction", "Food and Drink",
    "Health", "Historical", "Historical Fiction", "History", "Horror", "Humor", "Music",
    "Mystery", "New Adult", "Nonfiction", "Novels", "Paranormal", "Parenting", "Philosophy",
    "Poetry", "Politics", "Psychology", "Religion", "Romance", "Science", "Science Fiction",
    "Self Help", "Sequential Art", "Short Stories", "Spirituality", "Sports and Games",
    "Suspense", "Thriller", "Travel", "Womens Fiction", "Young Adult"
]


class APIHandler:
    def __init__(self, base_url: str) -> None:
        """
        Initialize the APIHandler with the base URL.
        Args:
            base_url (str): The base URL for the API.
        """
        self.base_url = base_url

    def _process_response(self, response: Response | None, payload: dict | None = None):
        """
        Process the API response and return a tuple of (json_data, status, payload).
        Args:
            response (Response | None): The API response object.
            payload (dict | None): The payload sent with the request.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """
        if response:
            try:
                return response.json(), True, payload
            except Exception:
                logger.warning("Response is not JSON serializable.")
                return None, True, payload
        return None, False, payload

    def send_request(self, method: str, endpoint: str, **kwargs) -> tuple[dict | None, bool, dict | None]:
        """
        Send an HTTP request to the API and return the response.
        Args:
            method (str): HTTP method (GET, POST, etc.).
            endpoint (str): API endpoint to call.
            **kwargs: Additional arguments for the request.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """
        url = f"{self.base_url}{endpoint}"
        payload_data = kwargs.get("json") or kwargs.get("params") or None
        try:
            response = request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            logger.info(f"[{method}] {url} - {response.status_code}")
            return self._process_response(response, payload_data)
        except exceptions.HTTPError as e:
            logger.error(f"[HTTPError] {url} - {e}")
        except exceptions.RequestException as e:
            logger.error(f"[RequestException] {url} - {e}")
        return None, False, payload_data

    @staticmethod
    def random_string(length: int = 8) -> str:
        return ''.join(choices(string.ascii_lowercase, k=length))

    def test_home(self) -> tuple[dict | None, bool, dict | None]:
        """
        Test the home endpoint.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """ 
        return self.send_request("GET", "/")

    def register_user(self, is_tester: bool = True, username: str = "", password: str = "") -> tuple[str | None, str | None]:
        """
        Registers a new user for testing purposes.

        Args:
            is_tester (bool): If True, a random username and password will be generated.
            username (str): Username to register (used only if is_tester is False).
            password (str): Password to register (used only if is_tester is False).

        Returns:
            tuple: A tuple containing the registered username and password if successful,
                otherwise (None, None).
        """
        if is_tester:
            username = f"user_{self.random_string()}"
            password = self.random_string()

        payload = {"username": username, "password": password}
        response, ok, _ = self.send_request("POST", "/api/v1/auth/register", json=payload)

        return (username, password) if ok else (None, None)


    def login_user(self, username: str, password: str) -> tuple[dict | None, bool, dict | None]:
        """
        Log in a user and return the access and refresh tokens.
        Args:
            username (str): The username of the user.
            password (str): The password of the user.
        Returns:
            tuple: A tuple containing the tokens, status (bool), and payload.
        """
        payload = {"username": username, "password": password}
        return self.send_request("POST", "/api/v1/auth/login", json=payload)

    def test_protected(self, token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Test a protected endpoint that requires authentication.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """ 
        return self._auth_get("/api/v1/auth/protected", token)

    def test_health(self, token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Test the health check endpoint.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """ 
        return self._auth_get("/api/v1/health/", token)

    def test_refresh(self, refresh_token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Refresh the access token using the refresh token.
        Args:
            refresh_token (str): The refresh token for authentication.
        Returns:
            tuple: A tuple containing the new tokens, status (bool), and payload.
        """
        payload = {"refresh_token": refresh_token}
        return self.send_request("POST", "/api/v1/auth/refresh", json=payload)

    def test_books_all(self, token: str) -> tuple[dict | None, bool, dict | None]: 
        """
        Get all books from the API.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """
        return self._auth_get("/api/v1/books/", token)

    def test_books_search(self, token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Search for books by title and/or category.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """
        category = choice(CATEGORIES)
        title = self.random_string(5) if randint(0, 1) else category
        params = {
            "title": title if randint(0, 1) else "",
            "category": category if randint(0, 1) else ""
        }
        logger.info(f"Searching books: title='{params['title']}', category='{params['category']}'")
        return self._auth_get("/api/v1/books/search", token, params=params)

    def test_books_top(self, token: str):
        """
        Get top-rated books from the API.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """
        params = {"limit": randint(1, 20)}
        return self._auth_get("/api/v1/books/top-rated", token, params=params)

    def test_books_price_range(self, token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Get books within a specified price range.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """
        min_price = randint(1, 20)
        max_price = min_price + randint(5, 30)
        params = {
            "min_price": min_price if randint(0, 1) else 0,
            "max_price": max_price if randint(0, 1) else 100
        }
        logger.info(f"Price range: {params['min_price']} - {params['max_price']}")
        return self._auth_get("/api/v1/books/price-range", token, params=params)

    def test_book_by_id(self, token: str):
        book_id = randint(1, 1000)
        return self._auth_get(f"/api/v1/books/{book_id}", token)

    def test_categories(self, token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Get all book categories from the API.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """     
        return self._auth_get("/api/v1/categories/", token)

    def test_stats_overview(self, token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Get all book categories from the API.
        Args:
            token (str): The access token for authentication.
            rns:
                tuple: A tuple containing the JSON data, status (bool), and payload.
        """         
        return self._auth_get("/api/v1/stats/overview", token)

    def test_stats_categories(self, token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Get all book categories from the API.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """         
        return self._auth_get("/api/v1/stats/categories", token)

    def test_ml_features(self, token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Get all book categories from the API.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """         
        return self._auth_get("/api/v1/ml/features", token)

    def test_ml_training_data(self, token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Get all book categories from the API.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """         
        return self._auth_get("/api/v1/ml/training-data", token)

    def test_ml_predictions(self, token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Get predictions for a random book based on price and category.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """
        payload = {
            "features": [{
                "price": round(uniform(5.0, 100.0), 2),
                "category": choice(CATEGORIES)
            }]
        }
        return self.send_request("POST", "/api/v1/ml/predictions", 
                                 headers=self._auth_header(token), 
                                 json=payload)

    def test_logs_list(self, token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Get a list of logs from the API.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """
        return self._auth_get("/api/v1/logs/", token)

    def test_logs_delete(self, token: str) -> tuple[dict | None, bool, dict | None]:
        """
        Get a list of logs from the API.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """
        return self.send_request("DELETE", "/api/v1/logs/", headers=self._auth_header(token))

    def _auth_get(self, endpoint: str, token: str, **kwargs) -> tuple[dict | None, bool, dict | None]:
        """
        Get a list of logs from the API.
        Args:
            token (str): The access token for authentication.
        Returns:
            tuple: A tuple containing the JSON data, status (bool), and payload.
        """
        return self.send_request("GET", endpoint, headers=self._auth_header(token), **kwargs)

    @staticmethod
    def _auth_header(token: str) -> dict:
        return {"Authorization": f"Bearer {token}"}
