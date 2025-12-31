"""Authentication schemas/DTOs"""

from pydantic import BaseModel, EmailStr


class TokenRequest(BaseModel):
    """Token request schema for login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str


class PasswordChangeRequest(BaseModel):
    """Password change request schema"""
    current_password: str
    new_password: str
