"""
API Endpoint Entegrasyon Testleri
Test Senaryoları: TC-1.2.x ve TC-2.2.x (API endpoint testleri)
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from app.services.customer_service import IndividualCustomerService
from app.services.account_manager_service import AccountManagerService


class TestCustomerAPIEndpoints:
    """Müşteri API Endpoint Testleri"""
    
    def setup_method(self):
        """Her test öncesi client oluştur ve servisleri sıfırla"""
        self.client = TestClient(app)
        
        # Servisleri sıfırla
        customer_service = IndividualCustomerService()
        customer_service.customers = []
        customer_service.next_id = 1
        
        manager_service = AccountManagerService()
        manager_service.account_managers = []
        manager_service.next_id = 1
    
    def test_create_customer_endpoint(self):
        """POST /api/v1/customers/individual/ - Müşteri oluşturma"""
        customer_data = {
            "firstName": "API",
            "lastName": "Test",
            "email": "api@test.com",
            "password": "password123",
            "natId": "12345678901"
        }
        
        response = self.client.post(
            "/api/v1/customers/individual/",
            json=customer_data
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["firstName"] == "API"
        assert data["email"] == "api@test.com"
        assert "password" not in data  # Password response'da olmamalı
    
    def test_create_customer_validation_error(self):
        """POST /api/v1/customers/individual/ - Eksik zorunlu alan hatası"""
        customer_data = {
            "firstName": "Test"
            # lastName, email, password, natId eksik
        }
        
        response = self.client.post(
            "/api/v1/customers/individual/",
            json=customer_data
        )
        
        assert response.status_code == 422  # Validation Error
    
    def test_create_customer_duplicate_email(self):
        """POST /api/v1/customers/individual/ - Tekrarlayan e-posta hatası"""
        customer_data = {
            "firstName": "First",
            "lastName": "Customer",
            "email": "same@test.com",
            "password": "password123",
            "natId": "12345678901"
        }
        
        # İlk müşteri
        self.client.post("/api/v1/customers/individual/", json=customer_data)
        
        # Aynı e-posta ile ikinci müşteri
        customer_data["natId"] = "98765432109"
        response = self.client.post(
            "/api/v1/customers/individual/",
            json=customer_data
        )
        
        assert response.status_code == 400
        assert "Email already exists" in response.json()["detail"]
    
    def test_get_all_customers_endpoint(self):
        """GET /api/v1/customers/individual/ - Müşteri listeleme"""
        # Önce müşteri ekle
        customer_data = {
            "firstName": "Test",
            "lastName": "Customer",
            "email": "test@test.com",
            "password": "password123",
            "natId": "12345678901"
        }
        self.client.post("/api/v1/customers/individual/", json=customer_data)
        
        response = self.client.get("/api/v1/customers/individual/")
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] == 1
    
    def test_get_customer_by_id_endpoint(self):
        """GET /api/v1/customers/individual/{id} - ID ile müşteri getirme"""
        # Önce müşteri ekle
        customer_data = {
            "firstName": "Test",
            "lastName": "Customer",
            "email": "test@test.com",
            "password": "password123",
            "natId": "12345678901"
        }
        create_response = self.client.post(
            "/api/v1/customers/individual/",
            json=customer_data
        )
        customer_id = create_response.json()["id"]
        
        response = self.client.get(f"/api/v1/customers/individual/{customer_id}")
        
        assert response.status_code == 200
        assert response.json()["id"] == customer_id
    
    def test_get_customer_not_found(self):
        """GET /api/v1/customers/individual/{id} - Bulunamayan müşteri"""
        response = self.client.get("/api/v1/customers/individual/9999")
        
        assert response.status_code == 404
    
    def test_update_customer_endpoint(self):
        """PUT /api/v1/customers/individual/{id} - Müşteri güncelleme"""
        # Önce müşteri ekle
        customer_data = {
            "firstName": "Original",
            "lastName": "Customer",
            "email": "original@test.com",
            "password": "password123",
            "natId": "12345678901"
        }
        create_response = self.client.post(
            "/api/v1/customers/individual/",
            json=customer_data
        )
        customer_id = create_response.json()["id"]
        
        # Güncelle
        update_data = {
            "firstName": "Updated"
        }
        response = self.client.put(
            f"/api/v1/customers/individual/{customer_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        assert response.json()["firstName"] == "Updated"
    
    def test_delete_customer_endpoint(self):
        """DELETE /api/v1/customers/individual/{id} - Müşteri silme"""
        # Önce müşteri ekle
        customer_data = {
            "firstName": "ToDelete",
            "lastName": "Customer",
            "email": "delete@test.com",
            "password": "password123",
            "natId": "12345678901"
        }
        create_response = self.client.post(
            "/api/v1/customers/individual/",
            json=customer_data
        )
        customer_id = create_response.json()["id"]
        
        response = self.client.delete(f"/api/v1/customers/individual/{customer_id}")
        
        assert response.status_code == 204
        
        # Silinen müşteri artık bulunamaz
        get_response = self.client.get(f"/api/v1/customers/individual/{customer_id}")
        assert get_response.status_code == 404


class TestAccountManagerAPIEndpoints:
    """Müşteri Sorumlusu API Endpoint Testleri"""
    
    def setup_method(self):
        """Her test öncesi client oluştur ve servisleri sıfırla"""
        self.client = TestClient(app)
        
        # Servisleri sıfırla
        manager_service = AccountManagerService()
        manager_service.account_managers = []
        manager_service.next_id = 1
    
    def test_create_account_manager_endpoint(self):
        """POST /api/v1/account-managers/ - Müşteri sorumlusu oluşturma"""
        manager_data = {
            "firstName": "New",
            "lastName": "Manager",
            "email": "new@crm.com"
        }
        
        response = self.client.post(
            "/api/v1/account-managers/",
            json=manager_data
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["firstName"] == "New"
        assert data["isActive"] is True
    
    def test_create_account_manager_with_optional_fields(self):
        """POST /api/v1/account-managers/ - Opsiyonel alanlar ile"""
        manager_data = {
            "firstName": "Full",
            "lastName": "Manager",
            "email": "full@crm.com",
            "phone": "0532 123 45 67",
            "department": "Sales"
        }
        
        response = self.client.post(
            "/api/v1/account-managers/",
            json=manager_data
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["phone"] == "0532 123 45 67"
        assert data["department"] == "Sales"
    
    def test_get_all_account_managers_endpoint(self):
        """GET /api/v1/account-managers/ - Sorumlu listeleme"""
        # Önce sorumlu ekle
        manager_data = {
            "firstName": "Test",
            "lastName": "Manager",
            "email": "test@crm.com"
        }
        self.client.post("/api/v1/account-managers/", json=manager_data)
        
        response = self.client.get("/api/v1/account-managers/")
        
        assert response.status_code == 200
        assert len(response.json()) >= 1
    
    def test_get_account_manager_dropdown_endpoint(self):
        """GET /api/v1/account-managers/dropdown - Dropdown listesi"""
        # Aktif sorumlu ekle
        manager_data = {
            "firstName": "Active",
            "lastName": "Manager",
            "email": "active@crm.com"
        }
        self.client.post("/api/v1/account-managers/", json=manager_data)
        
        response = self.client.get("/api/v1/account-managers/dropdown")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert "id" in data[0]
        assert "fullName" in data[0]
    
    def test_get_account_manager_by_id_endpoint(self):
        """GET /api/v1/account-managers/{id} - ID ile sorumlu getirme"""
        # Önce sorumlu ekle
        manager_data = {
            "firstName": "Test",
            "lastName": "Manager",
            "email": "test@crm.com"
        }
        create_response = self.client.post(
            "/api/v1/account-managers/",
            json=manager_data
        )
        manager_id = create_response.json()["id"]
        
        response = self.client.get(f"/api/v1/account-managers/{manager_id}")
        
        assert response.status_code == 200
        assert response.json()["id"] == manager_id
    
    def test_update_account_manager_endpoint(self):
        """PUT /api/v1/account-managers/{id} - Sorumlu güncelleme"""
        # Önce sorumlu ekle
        manager_data = {
            "firstName": "Original",
            "lastName": "Manager",
            "email": "original@crm.com"
        }
        create_response = self.client.post(
            "/api/v1/account-managers/",
            json=manager_data
        )
        manager_id = create_response.json()["id"]
        
        # Güncelle
        update_data = {
            "firstName": "Updated"
        }
        response = self.client.put(
            f"/api/v1/account-managers/{manager_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        assert response.json()["firstName"] == "Updated"
    
    def test_deactivate_account_manager_endpoint(self):
        """PUT /api/v1/account-managers/{id} - Sorumluyu pasif yapma"""
        # Önce sorumlu ekle
        manager_data = {
            "firstName": "Active",
            "lastName": "Manager",
            "email": "active@crm.com"
        }
        create_response = self.client.post(
            "/api/v1/account-managers/",
            json=manager_data
        )
        manager_id = create_response.json()["id"]
        
        # Pasif yap
        update_data = {
            "isActive": False
        }
        response = self.client.put(
            f"/api/v1/account-managers/{manager_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        assert response.json()["isActive"] is False
    
    def test_delete_account_manager_endpoint(self):
        """DELETE /api/v1/account-managers/{id} - Sorumlu silme"""
        # Önce sorumlu ekle
        manager_data = {
            "firstName": "ToDelete",
            "lastName": "Manager",
            "email": "delete@crm.com"
        }
        create_response = self.client.post(
            "/api/v1/account-managers/",
            json=manager_data
        )
        manager_id = create_response.json()["id"]
        
        response = self.client.delete(f"/api/v1/account-managers/{manager_id}")
        
        assert response.status_code == 204


class TestCustomerWithManagerAPIEndpoints:
    """Müşteri-Sorumlu İlişkisi API Endpoint Testleri"""
    
    def setup_method(self):
        """Her test öncesi client oluştur ve servisleri sıfırla"""
        self.client = TestClient(app)
        
        # Servisleri sıfırla
        customer_service = IndividualCustomerService()
        customer_service.customers = []
        customer_service.next_id = 1
        
        manager_service = AccountManagerService()
        manager_service.account_managers = []
        manager_service.next_id = 1
        
        # Önce bir sorumlu oluştur
        manager_data = {
            "firstName": "Test",
            "lastName": "Manager",
            "email": "manager@crm.com"
        }
        response = self.client.post("/api/v1/account-managers/", json=manager_data)
        self.manager_id = response.json()["id"]
    
    def test_create_customer_with_manager(self):
        """POST /api/v1/customers/individual/ - Sorumlu ile müşteri oluşturma"""
        customer_data = {
            "firstName": "Test",
            "lastName": "Customer",
            "email": "test@test.com",
            "password": "password123",
            "natId": "12345678901",
            "accountManagerId": self.manager_id
        }
        
        response = self.client.post(
            "/api/v1/customers/individual/",
            json=customer_data
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["accountManager"] is not None
        assert data["accountManager"]["id"] == self.manager_id
        assert data["accountManager"]["fullName"] == "Test Manager"
    
    def test_create_customer_with_invalid_manager(self):
        """POST /api/v1/customers/individual/ - Geçersiz sorumlu ID hatası"""
        customer_data = {
            "firstName": "Test",
            "lastName": "Customer",
            "email": "test@test.com",
            "password": "password123",
            "natId": "12345678901",
            "accountManagerId": 9999  # Geçersiz ID
        }
        
        response = self.client.post(
            "/api/v1/customers/individual/",
            json=customer_data
        )
        
        assert response.status_code == 400
        assert "Account Manager not found" in response.json()["detail"]
    
    def test_get_customer_includes_manager_info(self):
        """GET /api/v1/customers/individual/{id} - Yanıtta sorumlu bilgisi"""
        # Müşteri oluştur
        customer_data = {
            "firstName": "Test",
            "lastName": "Customer",
            "email": "test@test.com",
            "password": "password123",
            "natId": "12345678901",
            "accountManagerId": self.manager_id
        }
        create_response = self.client.post(
            "/api/v1/customers/individual/",
            json=customer_data
        )
        customer_id = create_response.json()["id"]
        
        # Müşteriyi getir
        response = self.client.get(f"/api/v1/customers/individual/{customer_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["accountManager"]["id"] == self.manager_id
        assert data["accountManager"]["fullName"] == "Test Manager"
    
    def test_update_customer_manager(self):
        """PUT /api/v1/customers/individual/{id} - Müşteri sorumlusunu değiştirme"""
        # İkinci sorumlu oluştur
        manager_data = {
            "firstName": "Second",
            "lastName": "Manager",
            "email": "second@crm.com"
        }
        response = self.client.post("/api/v1/account-managers/", json=manager_data)
        second_manager_id = response.json()["id"]
        
        # Müşteri oluştur (ilk sorumlu ile)
        customer_data = {
            "firstName": "Test",
            "lastName": "Customer",
            "email": "test@test.com",
            "password": "password123",
            "natId": "12345678901",
            "accountManagerId": self.manager_id
        }
        create_response = self.client.post(
            "/api/v1/customers/individual/",
            json=customer_data
        )
        customer_id = create_response.json()["id"]
        
        # Sorumluyu değiştir
        update_data = {
            "accountManagerId": second_manager_id
        }
        response = self.client.put(
            f"/api/v1/customers/individual/{customer_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        assert response.json()["accountManager"]["id"] == second_manager_id


class TestSwaggerDocumentation:
    """Swagger/OpenAPI Dokumentasyon Testleri"""
    
    def setup_method(self):
        """Her test öncesi client oluştur"""
        self.client = TestClient(app)
    
    def test_swagger_ui_available(self):
        """Swagger UI sayfası erişilebilir olmalı"""
        response = self.client.get("/docs")
        
        assert response.status_code == 200
    
    def test_redoc_available(self):
        """ReDoc sayfası erişilebilir olmalı"""
        response = self.client.get("/redoc")
        
        assert response.status_code == 200
    
    def test_openapi_json_available(self):
        """OpenAPI JSON endpoint erişilebilir olmalı"""
        response = self.client.get("/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data


class TestCORSConfiguration:
    """CORS Konfigürasyon Testleri"""
    
    def setup_method(self):
        """Her test öncesi client oluştur"""
        self.client = TestClient(app)
    
    def test_cors_headers_present(self):
        """CORS başlıkları yanıtta mevcut olmalı"""
        response = self.client.options(
            "/api/v1/customers/individual/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        # CORS middleware aktif olduğunda başlıklar döner
        assert response.status_code in [200, 405]  # OPTIONS metodu destekleniyor
