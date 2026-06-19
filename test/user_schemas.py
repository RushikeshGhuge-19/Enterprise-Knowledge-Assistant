from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    admin = "admin"
    user = "user"
    viewer = "viewer"


class UserSignUp(BaseModel):
    """Schema for user signup request."""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "secure_password_123"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login request."""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "secure_password_123"
            }
        }


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": 1
            }
        }


class UserResponse(BaseModel):
    """Schema for user response (no password)."""
    id: int
    email: str
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "role": "user",
                "created_at": "2024-01-15T10:30:00+00:00"
            }
        }
