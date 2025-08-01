from typing import Tuple, Optional, Dict, Any
from requests import post, get, exceptions
from datetime import datetime, timedelta

from config import (
    LOGIN_URL, 
    REGISTER_URL, 
    REFRESH_URL, 
    LOGS_URL, 
    ADMIN_CREDENTIALS, 
    REQUEST_TIMEOUT, 
    LOGS_TIMEOUT, 
    TOKEN_EXPIRY_MINUTES
)


class LogsAPI:
    """
    Class to handle API interactions for the BookOnTheTable dashboard.
    Handles authentication, token management, and fetching logs.
    """
    
    def __init__(self) -> None:
        """
        Initializes the API client with default values.
        """
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
        
    def authenticate(self) -> Tuple[bool, str]:
        """
        Authenticates the user using the provided credentials.
        """
        try:
            login_response = post(
                LOGIN_URL, 
                json=ADMIN_CREDENTIALS, 
                timeout=REQUEST_TIMEOUT
            )
            
            if login_response.status_code == 200:
                tokens = login_response.json()
                self._set_tokens(tokens)
                return True, "Authenticated successfully"
            
            elif login_response.status_code == 401:
                register_response = post(
                    REGISTER_URL, 
                    json=ADMIN_CREDENTIALS, 
                    timeout=REQUEST_TIMEOUT
                )
                
                if register_response.status_code in [200, 201]:
                    login_response = post(
                        LOGIN_URL, 
                        json=ADMIN_CREDENTIALS, 
                        timeout=REQUEST_TIMEOUT
                    )
                    if login_response.status_code == 200:
                        tokens = login_response.json()
                        self._set_tokens(tokens)
                        return True, "User registered and authenticated successfully"

        except exceptions.Timeout:
            return False, "Connection timed out"
        except exceptions.ConnectionError:
            return False, "Connection error"
        except Exception as e:
            return False, f"Authentication error: {str(e)}"

        return False, "Authentication failed"

    def _set_tokens(self, tokens: Dict[str, str]) -> None:
        """
        Sets the access and refresh tokens and calculates the token expiry time.
        Args:
            tokens (Dict[str, str]): Dictionary containing 'access_token' and 'refresh_token'
        """
        self.access_token = tokens.get('access_token')
        self.refresh_token = tokens.get('refresh_token')
        self.token_expiry = datetime.now() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
    
    def refresh_access_token(self) -> Tuple[bool, str]:
        """
        Refreshes the access token using the refresh token.
        If the refresh token is not available or expired, it re-authenticates.
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not self.refresh_token:
            return self.authenticate()
            
        try:
            refresh_response = post(
                REFRESH_URL, 
                json={"refresh_token": self.refresh_token},
                timeout=REQUEST_TIMEOUT
            )
            
            if refresh_response.status_code == 200:
                tokens = refresh_response.json()
                self.access_token = tokens.get('access_token')
                self.token_expiry = datetime.now() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
                return True, "Access token refreshed successfully"
            else:
                return self.authenticate()
                
        except Exception:
            return self.authenticate()
    
    def get_headers(self) -> Dict[str, str]:
        """
        Returns the headers for API requests, including the access token.
        If the access token is expired or not set, it refreshes the token.
        Returns:
            Dict[str, str]: Headers including Authorization and Content-Type
        """
        if not self.access_token or datetime.now() >= self.token_expiry:
            self.refresh_access_token()
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def fetch_logs(self, limit: int = 1000) -> Tuple[Optional[Any], str]:
        """
        Fetches logs from the API with a specified limit.
        Args:
            limit (int): Maximum number of logs to fetch
        Returns:
            Tuple[Optional[Any], str]: (logs data, message)
        """
        try:
            params = {"limit": limit}
            response = get(
                LOGS_URL, 
                params=params,
                headers=self.get_headers(),
                timeout=LOGS_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json(), "Logs loaded successfully"
            elif response.status_code == 401:
                success, msg = self.refresh_access_token()
                if success:
                    response = get(
                        LOGS_URL, 
                        params=params,
                        headers=self.get_headers(),
                        timeout=LOGS_TIMEOUT
                    )
                    if response.status_code == 200:
                        return response.json(), "Logs loaded after token refresh"

            return None, f"Error fetching logs: Status {response.status_code}"

        except exceptions.Timeout:
            return None, "Timeout fetching logs"
        except exceptions.ConnectionError:
            return None, "Connection error fetching logs"
        except Exception as e:
            return None, f"Error fetching logs: {str(e)}"