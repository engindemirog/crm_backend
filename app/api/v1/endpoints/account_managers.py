from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.account_manager import (
    AccountManagerCreate,
    AccountManagerResponse,
    AccountManagerUpdate,
    AccountManagerList,
    AccountManagerListItem
)
from app.services.account_manager_service import account_manager_service

router = APIRouter(
    prefix="/api/v1/account-managers",
    tags=["Account Managers"]
)


@router.post(
    "/",
    response_model=AccountManagerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yeni account manager oluştur"
)
async def create_account_manager(manager_data: AccountManagerCreate):
    """
    Yeni müşteri sorumlusu (account manager) oluşturur.
    
    - **firstName**: Ad
    - **lastName**: Soyad
    - **email**: Email adresi (unique)
    - **phone**: Telefon numarası (opsiyonel)
    - **department**: Departman (opsiyonel)
    """
    try:
        manager = account_manager_service.create_account_manager(manager_data)
        return {
            **manager.model_dump(),
            "fullName": f"{manager.firstName} {manager.lastName}"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=AccountManagerList,
    summary="Tüm account manager'ları listele"
)
async def get_all_account_managers():
    """
    Sistemdeki tüm müşteri sorumlularını listeler.
    """
    managers = account_manager_service.get_all()
    return {
        "total": len(managers),
        "accountManagers": [
            {**m.model_dump(), "fullName": f"{m.firstName} {m.lastName}"}
            for m in managers
        ]
    }


@router.get(
    "/dropdown",
    response_model=List[AccountManagerListItem],
    summary="Dropdown için account manager listesi"
)
async def get_account_managers_dropdown():
    """
    Açılır kutu (dropdown) için sadece aktif müşteri sorumlularının
    id ve fullName bilgilerini döner.
    """
    return account_manager_service.get_dropdown_list()


@router.get(
    "/{manager_id}",
    response_model=AccountManagerResponse,
    summary="ID'ye göre account manager getir"
)
async def get_account_manager(manager_id: int):
    """
    Belirtilen ID'ye sahip müşteri sorumlusunu getirir.
    """
    manager = account_manager_service.get_by_id(manager_id)
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account Manager with ID {manager_id} not found"
        )
    return {
        **manager.model_dump(),
        "fullName": f"{manager.firstName} {manager.lastName}"
    }


@router.put(
    "/{manager_id}",
    response_model=AccountManagerResponse,
    summary="Account manager bilgilerini güncelle"
)
async def update_account_manager(manager_id: int, manager_data: AccountManagerUpdate):
    """
    Belirtilen ID'ye sahip müşteri sorumlusunun bilgilerini günceller.
    """
    try:
        manager = account_manager_service.update_account_manager(manager_id, manager_data)
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account Manager with ID {manager_id} not found"
            )
        return {
            **manager.model_dump(),
            "fullName": f"{manager.firstName} {manager.lastName}"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{manager_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Account manager sil"
)
async def delete_account_manager(manager_id: int):
    """
    Belirtilen ID'ye sahip müşteri sorumlusunu siler.
    """
    success = account_manager_service.delete_account_manager(manager_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account Manager with ID {manager_id} not found"
        )
