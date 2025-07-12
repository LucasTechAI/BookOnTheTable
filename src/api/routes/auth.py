from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from datetime import timedelta

from api.services.auth_service import authenticate_user, create_user
from api.utils.jwt_handler import create_access_token, get_current_user
from api.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


class UserRequest(BaseModel):
    """
    UserRequest model for user registration and login.
    Contains fields for username and password.
    """
    username: str
    password: str


class TokenResponse(BaseModel):
    """
    TokenResponse model for returning JWT token.
    Contains fields for access token and token type.
    """
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=TokenResponse)
def register(data: UserRequest) -> TokenResponse:
    """
    Register a new user and return a JWT token.

    Args:
        data (UserRequest): The user registration data containing username and password.
    Returns:
        TokenResponse: A response containing the access token.
    """
    user = create_user(data.username, data.password)
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(user, expires_delta=token_expires)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(data: UserRequest) -> TokenResponse:
    """
    Authenticate a user and return a JWT token.
    Args:
        data (UserRequest): The user login data containing username and password.
    Returns:
        TokenResponse: A response containing the access token.
    """
    user = authenticate_user(data.username, data.password)
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(user, expires_delta=token_expires)
    return TokenResponse(access_token=token)


@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)) -> dict:
    """
    A protected route that requires authentication.
    Args:
        current_user (dict): The currently authenticated user.
    Returns:
        dict: A message confirming authenticated access.
    """
    return {
        "message": f"Authenticated access granted to {current_user['username']}!"
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(current_user: dict = Depends(get_current_user)) -> TokenResponse:
    """
    Refresh the JWT token for the current user.
    Args:
        current_user (dict): The currently authenticated user.
    Returns:
        TokenResponse: A response containing the new access token.
    Raises:
        HTTPException: If the current user is not authenticated.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user"
        )

    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_token = create_access_token(current_user, expires_delta=token_expires)

    return TokenResponse(access_token=new_token)