from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class AccountManager(BaseModel):
    """Müşteri Sorumlusu (Account Manager) Modeli"""
    id: Optional[int] = None
    firstName: str
    lastName: str
    email: EmailStr
    phone: Optional[str] = None
    department: Optional[str] = None
    isActive: bool = True
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True
    
    @property
    def fullName(self) -> str:
        return f"{self.firstName} {self.lastName}"
