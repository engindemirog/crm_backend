"""
Authentication Şemaları
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class UserType(str, Enum):
    """Kullanıcı tipleri"""
    CC = "cc"           # Customer Care / Müşteri Temsilcisi
    ADMIN = "admin"     # Sistem Yöneticisi


class LoginRequest(BaseModel):
    """Giriş isteği şeması"""
    username: str
    password: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "admin",
                "password": "admin123"
            }
        }
    }


class TokenResponse(BaseModel):
    """Token yanıt şeması"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserResponse"
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user": {
                    "id": 1,
                    "username": "admin",
                    "email": "admin@crm.com",
                    "fullName": "System Admin",
                    "userType": "admin"
                }
            }
        }
    }


class UserResponse(BaseModel):
    """Kullanıcı bilgi yanıtı"""
    id: int
    username: str
    email: str
    fullName: str
    userType: UserType
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "username": "admin",
                "email": "admin@crm.com",
                "fullName": "System Admin",
                "userType": "admin"
            }
        }
    }


class TokenData(BaseModel):
    """Token içeriği (JWT payload)"""
    user_id: int
    username: str
    user_type: UserType
    exp: Optional[int] = None


# Forward reference için güncelleme
TokenResponse.model_rebuild()
