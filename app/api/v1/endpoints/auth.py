"""
Authentication API Endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse, UserType
from app.services.auth_service import AuthService
from app.core.config import settings
from app.core.security import create_access_token, get_current_user, get_current_active_admin
from app.models.user import User
from typing import List


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
    responses={
        401: {"description": "Unauthorized - Invalid credentials"},
        403: {"description": "Forbidden - Insufficient permissions"}
    }
)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Kullanıcı Girişi",
    description="""
    Kullanıcı adı ve şifre ile giriş yapın.
    
    ## Fake Kullanıcılar:
    
    ### Admin Kullanıcıları:
    - **admin** / admin123 (System Admin)
    - **manager** / manager123 (John Manager)
    
    ### CC (Customer Care) Kullanıcıları:
    - **cc1** / cc123 (Ahmet Yılmaz)
    - **cc2** / cc123 (Mehmet Demir)
    - **cc3** / cc123 (Ayşe Kaya)
    
    ## Yanıt:
    Başarılı giriş sonrası JWT token ve kullanıcı bilgileri döner.
    Token'ı diğer API isteklerinde `Authorization: Bearer <token>` header'ında kullanın.
    """
)
async def login(login_data: LoginRequest):
    """
    Kullanıcı girişi - JWT token döndürür
    """
    auth_service = AuthService()
    
    # Kullanıcıyı doğrula
    user = auth_service.authenticate(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Access token oluştur
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "username": user.username,
            "user_type": user.userType.value
        },
        expires_delta=access_token_expires
    )
    
    # Kullanıcı response'u hazırla
    user_response = auth_service.get_user_response(user)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # saniye cinsinden
        user=user_response
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Mevcut Kullanıcı Bilgisi",
    description="Token ile giriş yapmış kullanıcının bilgilerini döndürür."
)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Mevcut kullanıcının bilgilerini getir
    """
    auth_service = AuthService()
    return auth_service.get_user_response(current_user)


@router.get(
    "/users",
    response_model=List[UserResponse],
    summary="Tüm Kullanıcılar (Admin)",
    description="Sistemdeki tüm kullanıcıları listeler. Sadece admin kullanabilir."
)
async def get_all_users(current_user: User = Depends(get_current_active_admin)):
    """
    Tüm kullanıcıları getir (Admin only)
    """
    auth_service = AuthService()
    users = auth_service.get_all_users()
    return [auth_service.get_user_response(u) for u in users]


@router.get(
    "/users/type/{user_type}",
    response_model=List[UserResponse],
    summary="Tipe Göre Kullanıcılar (Admin)",
    description="Belirtilen tipteki kullanıcıları listeler. Sadece admin kullanabilir."
)
async def get_users_by_type(
    user_type: UserType,
    current_user: User = Depends(get_current_active_admin)
):
    """
    Tipe göre kullanıcıları getir (Admin only)
    """
    auth_service = AuthService()
    users = auth_service.get_users_by_type(user_type)
    return [auth_service.get_user_response(u) for u in users]


@router.post(
    "/validate",
    response_model=UserResponse,
    summary="Token Doğrulama",
    description="Mevcut token'ın geçerli olup olmadığını kontrol eder."
)
async def validate_token(current_user: User = Depends(get_current_user)):
    """
    Token doğrulama - geçerli token için kullanıcı bilgisi döner
    """
    auth_service = AuthService()
    return auth_service.get_user_response(current_user)
