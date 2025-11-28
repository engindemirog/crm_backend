from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.customer import (
    IndividualCustomerCreate,
    IndividualCustomerResponse,
    IndividualCustomerUpdate,
    IndividualCustomerList
)
from app.services.customer_service import individual_customer_service

router = APIRouter(
    prefix="/api/v1/customers/individual",
    tags=["Individual Customers"]
)


@router.post(
    "/",
    response_model=IndividualCustomerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yeni bireysel müşteri oluştur"
)
async def create_individual_customer(customer_data: IndividualCustomerCreate):
    """
    Yeni bireysel müşteri oluşturur.
    
    - **firstName**: Müşterinin adı
    - **lastName**: Müşterinin soyadı
    - **email**: Müşterinin email adresi (unique)
    - **password**: Müşterinin şifresi (minimum 6 karakter)
    - **natId**: TC Kimlik Numarası (11 haneli, unique)
    - **fatherName**: Baba adı
    - **birthDate**: Doğum tarihi
    - **accountManagerId**: Müşteri sorumlusu ID (opsiyonel, dropdown'dan seçilir)
    """
    try:
        customer = individual_customer_service.create_customer(customer_data)
        return individual_customer_service.get_customer_response(customer)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=IndividualCustomerList,
    summary="Tüm bireysel müşterileri listele"
)
async def get_all_individual_customers():
    """
    Sistemdeki tüm bireysel müşterileri listeler.
    """
    customers = individual_customer_service.get_all_customers()
    return {
        "total": len(customers),
        "customers": [
            individual_customer_service.get_customer_response(c) for c in customers
        ]
    }


@router.get(
    "/{customer_id}",
    response_model=IndividualCustomerResponse,
    summary="ID'ye göre bireysel müşteri getir"
)
async def get_individual_customer(customer_id: int):
    """
    Belirtilen ID'ye sahip bireysel müşteriyi getirir.
    """
    customer = individual_customer_service.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
        )
    return individual_customer_service.get_customer_response(customer)


@router.put(
    "/{customer_id}",
    response_model=IndividualCustomerResponse,
    summary="Bireysel müşteri bilgilerini güncelle"
)
async def update_individual_customer(customer_id: int, customer_data: IndividualCustomerUpdate):
    """
    Belirtilen ID'ye sahip bireysel müşterinin bilgilerini günceller.
    """
    try:
        customer = individual_customer_service.update_customer(customer_id, customer_data)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found"
            )
        return individual_customer_service.get_customer_response(customer)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Bireysel müşteri sil"
)
async def delete_individual_customer(customer_id: int):
    """
    Belirtilen ID'ye sahip bireysel müşteriyi siler.
    """
    success = individual_customer_service.delete_customer(customer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
        )
