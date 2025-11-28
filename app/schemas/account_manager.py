from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class AccountManagerBase(BaseModel):
    """Account Manager Base Schema"""
    firstName: str = Field(..., min_length=2, max_length=50)
    lastName: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=100)


class AccountManagerCreate(AccountManagerBase):
    """Account Manager Oluşturma Schema"""
    pass


class AccountManagerUpdate(BaseModel):
    """Account Manager Güncelleme Schema"""
    firstName: Optional[str] = Field(None, min_length=2, max_length=50)
    lastName: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=100)
    isActive: Optional[bool] = None


class AccountManagerResponse(AccountManagerBase):
    """Account Manager Response Schema"""
    id: int
    fullName: str
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class AccountManagerListItem(BaseModel):
    """Dropdown için basit Account Manager listesi"""
    id: int
    fullName: str


class AccountManagerList(BaseModel):
    """Account Manager Listesi Response"""
    total: int
    accountManagers: list[AccountManagerResponse]
