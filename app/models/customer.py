from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class IndividualCustomer(BaseModel):
    """Bireysel Müşteri Modeli"""
    id: Optional[int] = None
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    natId: str  # TC Kimlik No
    fatherName: str
    birthDate: datetime
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True
