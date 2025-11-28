"""
Bireysel Müşteri Servis Birim Testleri
Test Senaryoları: TC-1.1.1.1 - TC-1.1.8.2
"""
import pytest
from datetime import datetime
from app.services.customer_service import IndividualCustomerService
from app.services.account_manager_service import AccountManagerService, account_manager_service
from app.schemas.customer import IndividualCustomerCreate, IndividualCustomerUpdate
from app.schemas.account_manager import AccountManagerCreate


class TestIndividualCustomerCreate:
    """FR-1.1.1: Bireysel Müşteri Ekleme Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'leri sıfırla"""
        # Account manager service'i sıfırla
        account_manager_service.account_managers = []
        account_manager_service.next_id = 1
        
        # Bir aktif account manager ekle
        manager_data = AccountManagerCreate(
            firstName="Test",
            lastName="Manager",
            email="test.manager@crm.com"
        )
        account_manager_service.create_account_manager(manager_data)
        
        # Customer service'i sıfırla
        self.service = IndividualCustomerService()
        self.service.customers = []
        self.service.next_id = 1
    
    def test_tc_1_1_1_1_successful_customer_creation(self):
        """TC-1.1.1.1: Başarılı bireysel müşteri ekleme"""
        customer_data = IndividualCustomerCreate(
            firstName="Test",
            lastName="User",
            email="test@example.com",
            password="123456",
            natId="12345678901",
            fatherName="Father",
            birthDate=datetime(1990, 1, 1)
        )
        
        customer = self.service.create_customer(customer_data)
        
        assert customer.id == 1
        assert customer.firstName == "Test"
        assert customer.lastName == "User"
        assert customer.email == "test@example.com"
        assert customer.natId == "12345678901"
        assert customer.createdAt is not None
        assert customer.updatedAt is not None
    
    def test_tc_1_1_1_2_customer_creation_with_account_manager(self):
        """TC-1.1.1.2: Müşteri sorumlusu ile bireysel müşteri ekleme"""
        customer_data = IndividualCustomerCreate(
            firstName="Test",
            lastName="User",
            email="test2@example.com",
            password="123456",
            natId="12345678902",
            fatherName="Father",
            birthDate=datetime(1990, 1, 1),
            accountManagerId=1
        )
        
        customer = self.service.create_customer(customer_data)
        
        assert customer.accountManagerId == 1
        
        # Response'da account manager bilgisi olmalı
        response = self.service.get_customer_response(customer)
        assert response["accountManager"] is not None
        assert response["accountManager"]["id"] == 1
    
    def test_tc_1_1_4_1_password_hashing(self):
        """TC-1.1.4.1: Şifre hashleme kontrolü"""
        customer_data = IndividualCustomerCreate(
            firstName="Test",
            lastName="User",
            email="hash@example.com",
            password="123456",
            natId="55555555555",
            fatherName="Father",
            birthDate=datetime(1990, 1, 1)
        )
        
        customer = self.service.create_customer(customer_data)
        
        # Şifre düz metin olarak saklanmamalı
        assert customer.password != "123456"
        # Bcrypt hash formatı kontrolü
        assert customer.password.startswith("$2")


class TestEmailUniqueness:
    """FR-1.1.2: E-posta Benzersizlik Kontrolü Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'leri sıfırla"""
        account_manager_service.account_managers = []
        account_manager_service.next_id = 1
        
        self.service = IndividualCustomerService()
        self.service.customers = []
        self.service.next_id = 1
        
        # İlk müşteriyi oluştur
        first_customer = IndividualCustomerCreate(
            firstName="First",
            lastName="User",
            email="existing@example.com",
            password="123456",
            natId="11111111111",
            fatherName="Father",
            birthDate=datetime(1990, 1, 1)
        )
        self.service.create_customer(first_customer)
    
    def test_tc_1_1_2_1_duplicate_email_on_create(self):
        """TC-1.1.2.1: Mevcut e-posta ile müşteri ekleme"""
        customer_data = IndividualCustomerCreate(
            firstName="Second",
            lastName="User",
            email="existing@example.com",  # Mevcut e-posta
            password="123456",
            natId="22222222222",
            fatherName="Father",
            birthDate=datetime(1990, 1, 1)
        )
        
        with pytest.raises(ValueError) as exc_info:
            self.service.create_customer(customer_data)
        
        assert "Email already exists" in str(exc_info.value)
    
    def test_tc_1_1_2_2_duplicate_email_on_update(self):
        """TC-1.1.2.2: Güncelleme ile mevcut e-posta atama"""
        # İkinci müşteriyi oluştur
        second_customer = IndividualCustomerCreate(
            firstName="Second",
            lastName="User",
            email="second@example.com",
            password="123456",
            natId="22222222222",
            fatherName="Father",
            birthDate=datetime(1990, 1, 1)
        )
        self.service.create_customer(second_customer)
        
        # İkinci müşterinin e-postasını birincinin e-postasıyla güncellemeye çalış
        update_data = IndividualCustomerUpdate(email="existing@example.com")
        
        with pytest.raises(ValueError) as exc_info:
            self.service.update_customer(2, update_data)
        
        assert "Email already exists" in str(exc_info.value)


class TestNatIdUniqueness:
    """FR-1.1.3: TC Kimlik No Benzersizlik Kontrolü Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'leri sıfırla"""
        account_manager_service.account_managers = []
        account_manager_service.next_id = 1
        
        self.service = IndividualCustomerService()
        self.service.customers = []
        self.service.next_id = 1
        
        # İlk müşteriyi oluştur
        first_customer = IndividualCustomerCreate(
            firstName="First",
            lastName="User",
            email="first@example.com",
            password="123456",
            natId="12345678901",
            fatherName="Father",
            birthDate=datetime(1990, 1, 1)
        )
        self.service.create_customer(first_customer)
    
    def test_tc_1_1_3_1_duplicate_nat_id_on_create(self):
        """TC-1.1.3.1: Mevcut TC Kimlik No ile müşteri ekleme"""
        customer_data = IndividualCustomerCreate(
            firstName="Second",
            lastName="User",
            email="second@example.com",
            password="123456",
            natId="12345678901",  # Mevcut TC Kimlik No
            fatherName="Father",
            birthDate=datetime(1990, 1, 1)
        )
        
        with pytest.raises(ValueError) as exc_info:
            self.service.create_customer(customer_data)
        
        assert "National ID already exists" in str(exc_info.value)
    
    def test_tc_1_1_3_2_duplicate_nat_id_on_update(self):
        """TC-1.1.3.2: Güncelleme ile mevcut TC Kimlik No atama"""
        # İkinci müşteriyi oluştur
        second_customer = IndividualCustomerCreate(
            firstName="Second",
            lastName="User",
            email="second@example.com",
            password="123456",
            natId="98765432109",
            fatherName="Father",
            birthDate=datetime(1990, 1, 1)
        )
        self.service.create_customer(second_customer)
        
        # İkinci müşterinin TC'sini birincinin TC'siyle güncellemeye çalış
        update_data = IndividualCustomerUpdate(natId="12345678901")
        
        with pytest.raises(ValueError) as exc_info:
            self.service.update_customer(2, update_data)
        
        assert "National ID already exists" in str(exc_info.value)


class TestCustomerListing:
    """FR-1.1.5: Bireysel Müşteri Listeleme Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'leri sıfırla"""
        account_manager_service.account_managers = []
        account_manager_service.next_id = 1
        
        self.service = IndividualCustomerService()
        self.service.customers = []
        self.service.next_id = 1
    
    def test_tc_1_1_5_1_list_all_customers(self):
        """TC-1.1.5.1: Tüm müşterileri listeleme"""
        # Birkaç müşteri oluştur
        for i in range(3):
            customer_data = IndividualCustomerCreate(
                firstName=f"User{i}",
                lastName="Test",
                email=f"user{i}@example.com",
                password="123456",
                natId=f"1111111111{i}",
                fatherName="Father",
                birthDate=datetime(1990, 1, 1)
            )
            self.service.create_customer(customer_data)
        
        customers = self.service.get_all_customers()
        
        assert len(customers) == 3
    
    def test_tc_1_1_5_2_empty_customer_list(self):
        """TC-1.1.5.2: Boş müşteri listesi"""
        customers = self.service.get_all_customers()
        
        assert len(customers) == 0


class TestCustomerDetail:
    """FR-1.1.6: Bireysel Müşteri Detay Görüntüleme Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'leri sıfırla"""
        account_manager_service.account_managers = []
        account_manager_service.next_id = 1
        
        self.service = IndividualCustomerService()
        self.service.customers = []
        self.service.next_id = 1
        
        # Bir müşteri oluştur
        customer_data = IndividualCustomerCreate(
            firstName="Test",
            lastName="User",
            email="test@example.com",
            password="123456",
            natId="12345678901",
            fatherName="Father",
            birthDate=datetime(1990, 1, 1)
        )
        self.service.create_customer(customer_data)
    
    def test_tc_1_1_6_1_get_customer_by_valid_id(self):
        """TC-1.1.6.1: Geçerli ID ile müşteri görüntüleme"""
        customer = self.service.get_customer_by_id(1)
        
        assert customer is not None
        assert customer.id == 1
        assert customer.firstName == "Test"
    
    def test_tc_1_1_6_2_get_customer_by_invalid_id(self):
        """TC-1.1.6.2: Geçersiz ID ile müşteri görüntüleme"""
        customer = self.service.get_customer_by_id(9999)
        
        assert customer is None


class TestCustomerUpdate:
    """FR-1.1.7: Bireysel Müşteri Güncelleme Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'leri sıfırla"""
        account_manager_service.account_managers = []
        account_manager_service.next_id = 1
        
        # Account manager ekle
        manager_data = AccountManagerCreate(
            firstName="Test",
            lastName="Manager",
            email="manager@crm.com"
        )
        account_manager_service.create_account_manager(manager_data)
        
        # İkinci account manager ekle
        manager_data2 = AccountManagerCreate(
            firstName="Second",
            lastName="Manager",
            email="manager2@crm.com"
        )
        account_manager_service.create_account_manager(manager_data2)
        
        self.service = IndividualCustomerService()
        self.service.customers = []
        self.service.next_id = 1
        
        # Bir müşteri oluştur
        customer_data = IndividualCustomerCreate(
            firstName="Original",
            lastName="Name",
            email="original@example.com",
            password="123456",
            natId="12345678901",
            fatherName="Father",
            birthDate=datetime(1990, 1, 1),
            accountManagerId=1
        )
        self.service.create_customer(customer_data)
    
    def test_tc_1_1_7_1_successful_customer_update(self):
        """TC-1.1.7.1: Başarılı müşteri güncelleme"""
        update_data = IndividualCustomerUpdate(
            firstName="Updated",
            lastName="User"
        )
        
        customer = self.service.update_customer(1, update_data)
        
        assert customer.firstName == "Updated"
        assert customer.lastName == "User"
    
    def test_tc_1_1_7_2_partial_update(self):
        """TC-1.1.7.2: Kısmi güncelleme (diğer alanlar değişmemeli)"""
        original_email = self.service.get_customer_by_id(1).email
        
        update_data = IndividualCustomerUpdate(firstName="OnlyName")
        customer = self.service.update_customer(1, update_data)
        
        assert customer.firstName == "OnlyName"
        assert customer.email == original_email  # E-posta değişmemeli
    
    def test_tc_1_1_7_3_update_account_manager(self):
        """TC-1.1.7.3: Müşteri sorumlusu güncelleme"""
        update_data = IndividualCustomerUpdate(accountManagerId=2)
        
        customer = self.service.update_customer(1, update_data)
        
        assert customer.accountManagerId == 2
    
    def test_tc_1_1_7_4_update_nonexistent_customer(self):
        """TC-1.1.7.4: Var olmayan müşteri güncelleme"""
        update_data = IndividualCustomerUpdate(firstName="Test")
        
        customer = self.service.update_customer(9999, update_data)
        
        assert customer is None


class TestCustomerDelete:
    """FR-1.1.8: Bireysel Müşteri Silme Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'leri sıfırla"""
        account_manager_service.account_managers = []
        account_manager_service.next_id = 1
        
        self.service = IndividualCustomerService()
        self.service.customers = []
        self.service.next_id = 1
        
        # Bir müşteri oluştur
        customer_data = IndividualCustomerCreate(
            firstName="ToDelete",
            lastName="User",
            email="delete@example.com",
            password="123456",
            natId="12345678901",
            fatherName="Father",
            birthDate=datetime(1990, 1, 1)
        )
        self.service.create_customer(customer_data)
    
    def test_tc_1_1_8_1_successful_customer_delete(self):
        """TC-1.1.8.1: Başarılı müşteri silme"""
        result = self.service.delete_customer(1)
        
        assert result is True
        assert self.service.get_customer_by_id(1) is None
    
    def test_tc_1_1_8_2_delete_nonexistent_customer(self):
        """TC-1.1.8.2: Var olmayan müşteri silme"""
        result = self.service.delete_customer(9999)
        
        assert result is False
