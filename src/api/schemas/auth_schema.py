from pydantic import BaseModel, Field

class AuthTokenResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field("bearer", example="bearer")


class RegisterError(BaseModel):
    detail: str = Field("Username already exists", example="Username already exists")


class LoginError(BaseModel):
    detail: str = Field("Invalid credentials", example="Invalid username or password")


class AuthError(BaseModel):
    detail: str = Field("Unauthorized", example="Could not validate credentials")


class RefreshTokenError(BaseModel):
    detail: str = Field("Invalid user", example="User not authenticated or token expired")


class ProtectedResponse(BaseModel):
    message: str = Field(..., example="Authenticated access granted to lucas_dev!")


class RefreshTokenResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field("bearer", example="bearer")


class UserRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthUserRequest(BaseModel):
    username: str = Field(..., example="admin", description="Username of the user")
    password: str = Field(..., example="admin", description="Password of the user")

    class Config:
        title = "AuthUserRequest"
        schema_extra = {
            "summary": "User login or registration payload",
            "description": "Schema used to receive login or registration credentials.",
            "example": {
                "username": "lucas_dev",
                "password": "123secure"
            }
        }


class AuthTokenResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(default="bearer", example="bearer")

    class Config:
        title = "AuthTokenResponse"
        schema_extra = {
            "summary": "Access token",
            "description": "JWT token returned after successful login or registration.",
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class RegisterRequest(AuthUserRequest):
    """
    Schema for user registration input.
    """
    class Config:
        title = "RegisterRequest"
        schema_extra = {
            "example": {
                "username": "lucas_dev",
                "password": "123secure"
            },
            "summary": "User registration",
            "description": "Used for registering a new user."
        }

class LoginRequest(AuthUserRequest):
    """
    Schema for user login input.
    """
    class Config:
        title = "LoginRequest"
        schema_extra = {
            "example": {
                "username": "lucas_dev",
                "password": "123secure"
            },
            "summary": "User login",
            "description": "Used for logging in an existing user."
        }

class ProtectedResponse(BaseModel):
    message: str = Field(..., example="Authenticated access granted to lucas_dev!")

    class Config:
        title = "ProtectedResponse"
        schema_extra = {
            "summary": "Protected endpoint response",
            "description": "Returned when user is successfully authenticated.",
            "example": {
                "message": "Authenticated access granted to lucas_dev!"
            }
        }

class RefreshTokenResponse(AuthTokenResponse):
    """
    JWT token returned when refreshing an expired one.
    """
    class Config:
        title = "RefreshTokenResponse"
        schema_extra = {
            "summary": "Refreshed JWT",
            "description": "A refreshed JWT token.",
            "example": {
                "access_token": "new.jwt.token.here",
                "token_type": "bearer"
            }
        }
