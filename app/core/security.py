"""
JWT Token Utilities
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.schemas.auth import TokenData, UserType
from app.services.auth_service import AuthService


# Bearer token için security scheme
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWT access token oluştur
    
    Args:
        data: Token'a eklenecek veriler
        expires_delta: Token süresi (opsiyonel)
        
    Returns:
        JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    JWT token doğrula ve decode et
    
    Args:
        token: JWT token string
        
    Returns:
        TokenData veya None
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        user_id: int = payload.get("user_id")
        username: str = payload.get("username")
        user_type: str = payload.get("user_type")
        
        if user_id is None or username is None:
            return None
        
        return TokenData(
            user_id=user_id,
            username=username,
            user_type=UserType(user_type)
        )
    except JWTError:
        return None


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Mevcut kullanıcıyı token'dan al (Dependency)
    
    Args:
        credentials: Bearer token credentials
        
    Returns:
        User objesi
        
    Raises:
        HTTPException: Token geçersiz veya kullanıcı bulunamadı
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    token_data = verify_token(token)
    
    if token_data is None:
        raise credentials_exception
    
    auth_service = AuthService()
    user = auth_service.get_user_by_id(token_data.user_id)
    
    if user is None:
        raise credentials_exception
    
    if not user.isActive:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_active_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Mevcut admin kullanıcıyı al (Dependency)
    
    Raises:
        HTTPException: Kullanıcı admin değilse
    """
    user = get_current_user(credentials)
    
    if user.userType != UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    )
):
    """
    Opsiyonel kullanıcı kontrolü - token yoksa None döner
    """
    if credentials is None:
        return None
    
    try:
        return get_current_user(credentials)
    except HTTPException:
        return None
