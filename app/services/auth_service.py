"""
Authentication Service - Fake kullanıcılar ile giriş işlemleri
"""
from typing import Optional, List
from datetime import datetime
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.auth import UserType, UserResponse


# Password hashing için context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication servisi - Singleton pattern"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Fake kullanıcıları başlat"""
        self.users: List[User] = []
        self._create_fake_users()
    
    def _create_fake_users(self):
        """Fake kullanıcıları oluştur"""
        fake_users_data = [
            # Admin kullanıcıları
            {
                "id": 1,
                "username": "admin",
                "email": "admin@crm.com",
                "password": "admin123",
                "firstName": "System",
                "lastName": "Admin",
                "userType": UserType.ADMIN
            },
            {
                "id": 2,
                "username": "manager",
                "email": "manager@crm.com",
                "password": "manager123",
                "firstName": "John",
                "lastName": "Manager",
                "userType": UserType.ADMIN
            },
            # CC (Customer Care) kullanıcıları
            {
                "id": 3,
                "username": "cc1",
                "email": "cc1@crm.com",
                "password": "cc123",
                "firstName": "Ahmet",
                "lastName": "Yılmaz",
                "userType": UserType.CC
            },
            {
                "id": 4,
                "username": "cc2",
                "email": "cc2@crm.com",
                "password": "cc123",
                "firstName": "Mehmet",
                "lastName": "Demir",
                "userType": UserType.CC
            },
            {
                "id": 5,
                "username": "cc3",
                "email": "cc3@crm.com",
                "password": "cc123",
                "firstName": "Ayşe",
                "lastName": "Kaya",
                "userType": UserType.CC
            },
        ]
        
        for user_data in fake_users_data:
            # Şifreyi hashle
            hashed_password = pwd_context.hash(user_data["password"])
            
            user = User(
                id=user_data["id"],
                username=user_data["username"],
                email=user_data["email"],
                password=hashed_password,
                firstName=user_data["firstName"],
                lastName=user_data["lastName"],
                userType=user_data["userType"],
                isActive=True,
                createdAt=datetime.now()
            )
            self.users.append(user)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Şifre doğrulama"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Kullanıcı adına göre kullanıcı bul"""
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """ID'ye göre kullanıcı bul"""
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Email'e göre kullanıcı bul"""
        for user in self.users:
            if user.email == email:
                return user
        return None
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Kullanıcı kimlik doğrulama
        
        Args:
            username: Kullanıcı adı
            password: Şifre (plain text)
            
        Returns:
            Doğrulama başarılıysa User, değilse None
        """
        user = self.get_user_by_username(username)
        
        if not user:
            return None
        
        if not user.isActive:
            return None
            
        if not self.verify_password(password, user.password):
            return None
        
        return user
    
    def get_user_response(self, user: User) -> UserResponse:
        """User modelini UserResponse'a dönüştür"""
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            fullName=user.fullName,
            userType=user.userType
        )
    
    def get_all_users(self) -> List[User]:
        """Tüm kullanıcıları getir (admin için)"""
        return self.users
    
    def get_users_by_type(self, user_type: UserType) -> List[User]:
        """Tipe göre kullanıcıları getir"""
        return [u for u in self.users if u.userType == user_type]
