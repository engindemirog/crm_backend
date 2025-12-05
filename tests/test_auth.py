"""
Authentication Birim Testleri
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from app.services.auth_service import AuthService
from app.schemas.auth import UserType


class TestAuthService:
    """AuthService birim testleri"""
    
    def setup_method(self):
        """Her test öncesi service'i al"""
        self.auth_service = AuthService()
    
    def test_fake_users_created(self):
        """Fake kullanıcılar oluşturulmuş olmalı"""
        users = self.auth_service.get_all_users()
        assert len(users) == 5  # 2 admin + 3 cc
    
    def test_authenticate_valid_admin(self):
        """Geçerli admin kullanıcı ile giriş"""
        user = self.auth_service.authenticate("admin", "admin123")
        
        assert user is not None
        assert user.username == "admin"
        assert user.userType == UserType.ADMIN
    
    def test_authenticate_valid_cc(self):
        """Geçerli CC kullanıcı ile giriş"""
        user = self.auth_service.authenticate("cc1", "cc123")
        
        assert user is not None
        assert user.username == "cc1"
        assert user.userType == UserType.CC
    
    def test_authenticate_invalid_username(self):
        """Geçersiz kullanıcı adı ile giriş"""
        user = self.auth_service.authenticate("invalid", "admin123")
        
        assert user is None
    
    def test_authenticate_invalid_password(self):
        """Geçersiz şifre ile giriş"""
        user = self.auth_service.authenticate("admin", "wrongpassword")
        
        assert user is None
    
    def test_get_user_by_username(self):
        """Kullanıcı adına göre kullanıcı bulma"""
        user = self.auth_service.get_user_by_username("manager")
        
        assert user is not None
        assert user.email == "manager@crm.com"
    
    def test_get_user_by_id(self):
        """ID'ye göre kullanıcı bulma"""
        user = self.auth_service.get_user_by_id(1)
        
        assert user is not None
        assert user.username == "admin"
    
    def test_get_users_by_type_admin(self):
        """Admin tipindeki kullanıcıları getir"""
        admins = self.auth_service.get_users_by_type(UserType.ADMIN)
        
        assert len(admins) == 2
        assert all(u.userType == UserType.ADMIN for u in admins)
    
    def test_get_users_by_type_cc(self):
        """CC tipindeki kullanıcıları getir"""
        cc_users = self.auth_service.get_users_by_type(UserType.CC)
        
        assert len(cc_users) == 3
        assert all(u.userType == UserType.CC for u in cc_users)


class TestAuthAPIEndpoints:
    """Auth API endpoint testleri"""
    
    def setup_method(self):
        """Her test öncesi client oluştur"""
        self.client = TestClient(app)
    
    def test_login_success_admin(self):
        """Başarılı admin girişi"""
        response = self.client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "admin"
        assert data["user"]["userType"] == "admin"
    
    def test_login_success_cc(self):
        """Başarılı CC kullanıcı girişi"""
        response = self.client.post(
            "/api/v1/auth/login",
            json={"username": "cc1", "password": "cc123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["userType"] == "cc"
    
    def test_login_invalid_credentials(self):
        """Geçersiz kimlik bilgileri ile giriş"""
        response = self.client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "wrongpass"}
        )
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self):
        """Var olmayan kullanıcı ile giriş"""
        response = self.client.post(
            "/api/v1/auth/login",
            json={"username": "notexist", "password": "password"}
        )
        
        assert response.status_code == 401
    
    def test_get_current_user_with_valid_token(self):
        """Geçerli token ile kullanıcı bilgisi alma"""
        # Önce login ol
        login_response = self.client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        
        # Token ile kullanıcı bilgisi al
        response = self.client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "admin"
        assert data["userType"] == "admin"
    
    def test_get_current_user_without_token(self):
        """Token olmadan kullanıcı bilgisi alma"""
        response = self.client.get("/api/v1/auth/me")
        
        assert response.status_code == 403  # Forbidden (no credentials)
    
    def test_get_current_user_with_invalid_token(self):
        """Geçersiz token ile kullanıcı bilgisi alma"""
        response = self.client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token_here"}
        )
        
        assert response.status_code == 401
    
    def test_validate_token_endpoint(self):
        """Token doğrulama endpoint'i"""
        # Önce login ol
        login_response = self.client.post(
            "/api/v1/auth/login",
            json={"username": "cc2", "password": "cc123"}
        )
        token = login_response.json()["access_token"]
        
        # Token'ı doğrula
        response = self.client.post(
            "/api/v1/auth/validate",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "cc2"
    
    def test_get_all_users_admin_only(self):
        """Tüm kullanıcıları listeleme (admin only)"""
        # Admin olarak login
        login_response = self.client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        
        response = self.client.get(
            "/api/v1/auth/users",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert len(response.json()) == 5
    
    def test_get_all_users_cc_forbidden(self):
        """CC kullanıcı tüm kullanıcıları listeleyemez"""
        # CC olarak login
        login_response = self.client.post(
            "/api/v1/auth/login",
            json={"username": "cc1", "password": "cc123"}
        )
        token = login_response.json()["access_token"]
        
        response = self.client.get(
            "/api/v1/auth/users",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 403
        assert "Admin privileges required" in response.json()["detail"]
    
    def test_get_users_by_type(self):
        """Tipe göre kullanıcıları listeleme"""
        # Admin olarak login
        login_response = self.client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        
        response = self.client.get(
            "/api/v1/auth/users/type/cc",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(u["userType"] == "cc" for u in data)


class TestTokenExpiry:
    """Token süre sonu testleri"""
    
    def setup_method(self):
        """Her test öncesi client oluştur"""
        self.client = TestClient(app)
    
    def test_token_includes_expiry(self):
        """Token yanıtında süre bilgisi olmalı"""
        response = self.client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        
        data = response.json()
        assert "expires_in" in data
        assert data["expires_in"] > 0  # Saniye cinsinden
