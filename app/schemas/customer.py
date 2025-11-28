from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class AccountManagerInfo(BaseModel):
    """Account Manager bilgisi için nested schema"""
    id: int
    fullName: str


class IndividualCustomerBase(BaseModel):
    """Bireysel Müşteri Base Schema"""
    firstName: str = Field(..., min_length=2, max_length=50)
    lastName: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    natId: str = Field(..., min_length=11, max_length=11, pattern=r'^\d{11}$')
    fatherName: str = Field(..., min_length=2, max_length=50)
    birthDate: datetime
    accountManagerId: Optional[int] = Field(None, description="Müşteri Sorumlusu ID")


class IndividualCustomerCreate(IndividualCustomerBase):
    """Bireysel Müşteri Oluşturma Schema"""
    password: str = Field(..., min_length=6, max_length=100)


class IndividualCustomerUpdate(BaseModel):
    """Bireysel Müşteri Güncelleme Schema"""
    firstName: Optional[str] = Field(None, min_length=2, max_length=50)
    lastName: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    natId: Optional[str] = Field(None, min_length=11, max_length=11, pattern=r'^\d{11}$')
    fatherName: Optional[str] = Field(None, min_length=2, max_length=50)
    birthDate: Optional[datetime] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    accountManagerId: Optional[int] = Field(None, description="Müşteri Sorumlusu ID")


class IndividualCustomerResponse(IndividualCustomerBase):
    """Bireysel Müşteri Response Schema"""
    id: int
    accountManager: Optional[AccountManagerInfo] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class IndividualCustomerList(BaseModel):
    """Bireysel Müşteri Listesi Response"""
    total: int
    customers: list[IndividualCustomerResponse]
