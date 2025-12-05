"""
User Model - Fake kullanıcılar için
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.schemas.auth import UserType


class User(BaseModel):
    """Kullanıcı modeli"""
    id: int
    username: str
    email: str
    password: str  # Hashlenmiş şifre
    firstName: str
    lastName: str
    userType: UserType
    isActive: bool = True
    createdAt: datetime = datetime.now()
    
    @property
    def fullName(self) -> str:
        return f"{self.firstName} {self.lastName}"
