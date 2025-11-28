import pytest
from fastapi.testclient import TestClient
from datetime import datetime

# Test için service instance'larını resetleme
from app.services.account_manager_service import AccountManagerService
from app.services.customer_service import IndividualCustomerService


@pytest.fixture
def account_manager_service():
    """Her test için temiz bir AccountManagerService instance'ı"""
    service = AccountManagerService()
    # Fake verileri temizle ve test için yeniden oluştur
    service.account_managers = []
    service.next_id = 1
    return service


@pytest.fixture
def customer_service(account_manager_service):
    """Her test için temiz bir IndividualCustomerService instance'ı"""
    # Account manager service'i önce hazırla
    from app.services import account_manager_service as ams
    ams.account_manager_service.account_managers = account_manager_service.account_managers
    ams.account_manager_service.next_id = account_manager_service.next_id
    
    service = IndividualCustomerService()
    service.customers = []
    service.next_id = 1
    return service


@pytest.fixture
def test_client():
    """FastAPI test client"""
    from main import app
    
    # Service'leri resetle
    from app.services.account_manager_service import account_manager_service
    from app.services.customer_service import individual_customer_service
    
    # Account Manager fake verilerini sıfırla ve yeniden oluştur
    account_manager_service.account_managers = []
    account_manager_service.next_id = 1
    account_manager_service._initialize_fake_data()
    
    # Customer fake verilerini sıfırla ve yeniden oluştur
    individual_customer_service.customers = []
    individual_customer_service.next_id = 1
    individual_customer_service._initialize_fake_data()
    
    return TestClient(app)


@pytest.fixture
def sample_customer_data():
    """Örnek müşteri verisi"""
    return {
        "firstName": "Test",
        "lastName": "User",
        "email": "test.user@example.com",
        "password": "password123",
        "natId": "55555555555",
        "fatherName": "Father",
        "birthDate": "1990-05-15T00:00:00"
    }


@pytest.fixture
def sample_account_manager_data():
    """Örnek account manager verisi"""
    return {
        "firstName": "Test",
        "lastName": "Manager",
        "email": "test.manager@crm.com",
        "phone": "0532 999 88 77",
        "department": "Test Departmanı"
    }
