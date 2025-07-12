from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from api.config import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Generates a JWT access token with an expiration time.

    Args:
        data (Dict[str, Any]): Data to encode into the token.
        expires_delta (Optional[timedelta]): Optional time delta for token expiration.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes a JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        Optional[Dict[str, Any]]: The token payload if valid, or None if invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Retrieves the current user from the JWT token.

    Args:
        token (str): JWT token extracted from the request.

    Returns:
        Dict[str, Any]: Payload with user info.

    Raises:
        HTTPException: If the token is invalid or user data is missing.
    """
    payload = decode_token(token)
    if payload is None or "username" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return {"username": payload["username"]}