"""
Müşteri Sorumlusu (Account Manager) Servis Birim Testleri
Test Senaryoları: TC-2.1.1.1 - TC-2.1.7.2
"""
import pytest
from datetime import datetime
from app.services.account_manager_service import AccountManagerService
from app.schemas.account_manager import AccountManagerCreate, AccountManagerUpdate


class TestAccountManagerCreate:
    """FR-2.1.1: Müşteri Sorumlusu Ekleme Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'i sıfırla"""
        self.service = AccountManagerService()
        self.service.account_managers = []
        self.service.next_id = 1
    
    def test_tc_2_1_1_1_successful_account_manager_creation(self):
        """TC-2.1.1.1: Başarılı müşteri sorumlusu ekleme"""
        manager_data = AccountManagerCreate(
            firstName="Yeni",
            lastName="Manager",
            email="manager@crm.com"
        )
        
        manager = self.service.create_account_manager(manager_data)
        
        assert manager.id == 1
        assert manager.firstName == "Yeni"
        assert manager.lastName == "Manager"
        assert manager.email == "manager@crm.com"
        assert manager.isActive is True
        assert manager.createdAt is not None
        assert manager.updatedAt is not None
    
    def test_tc_2_1_1_2_account_manager_with_optional_fields(self):
        """TC-2.1.1.2: Opsiyonel alanlar ile müşteri sorumlusu ekleme"""
        manager_data = AccountManagerCreate(
            firstName="Tam",
            lastName="Manager",
            email="tam@crm.com",
            phone="0532 123 45 67",
            department="Kurumsal Satış"
        )
        
        manager = self.service.create_account_manager(manager_data)
        
        assert manager.phone == "0532 123 45 67"
        assert manager.department == "Kurumsal Satış"
    
    def test_full_name_property(self):
        """Account manager fullName özelliği testi"""
        manager_data = AccountManagerCreate(
            firstName="Test",
            lastName="Manager",
            email="test@crm.com"
        )
        
        manager = self.service.create_account_manager(manager_data)
        
        assert manager.fullName == "Test Manager"


class TestAccountManagerEmailUniqueness:
    """FR-2.1.2: E-posta Benzersizlik Kontrolü Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'i sıfırla"""
        self.service = AccountManagerService()
        self.service.account_managers = []
        self.service.next_id = 1
        
        # İlk manager'ı oluştur
        first_manager = AccountManagerCreate(
            firstName="First",
            lastName="Manager",
            email="existing@crm.com"
        )
        self.service.create_account_manager(first_manager)
    
    def test_tc_2_1_2_1_duplicate_email_on_create(self):
        """TC-2.1.2.1: Mevcut e-posta ile müşteri sorumlusu ekleme"""
        manager_data = AccountManagerCreate(
            firstName="Second",
            lastName="Manager",
            email="existing@crm.com"  # Mevcut e-posta
        )
        
        with pytest.raises(ValueError) as exc_info:
            self.service.create_account_manager(manager_data)
        
        assert "Email already exists" in str(exc_info.value)


class TestAccountManagerListing:
    """FR-2.1.3: Müşteri Sorumlusu Listeleme Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'i sıfırla"""
        self.service = AccountManagerService()
        self.service.account_managers = []
        self.service.next_id = 1
    
    def test_tc_2_1_3_1_list_all_account_managers(self):
        """TC-2.1.3.1: Tüm müşteri sorumlularını listeleme"""
        # Birkaç manager oluştur
        for i in range(3):
            manager_data = AccountManagerCreate(
                firstName=f"Manager{i}",
                lastName="Test",
                email=f"manager{i}@crm.com"
            )
            self.service.create_account_manager(manager_data)
        
        managers = self.service.get_all()
        
        assert len(managers) == 3


class TestAccountManagerDropdown:
    """FR-2.1.4: Müşteri Sorumlusu Dropdown Listesi Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'i sıfırla"""
        self.service = AccountManagerService()
        self.service.account_managers = []
        self.service.next_id = 1
        
        # Aktif manager
        active_manager = AccountManagerCreate(
            firstName="Active",
            lastName="Manager",
            email="active@crm.com"
        )
        self.service.create_account_manager(active_manager)
        
        # Pasif manager oluştur ve pasif yap
        inactive_manager = AccountManagerCreate(
            firstName="Inactive",
            lastName="Manager",
            email="inactive@crm.com"
        )
        manager = self.service.create_account_manager(inactive_manager)
        self.service.update_account_manager(
            manager.id, 
            AccountManagerUpdate(isActive=False)
        )
    
    def test_tc_2_1_4_1_dropdown_only_active_managers(self):
        """TC-2.1.4.1: Dropdown için sadece aktif müşteri sorumluları"""
        dropdown = self.service.get_dropdown_list()
        
        # Sadece aktif olanlar görünmeli
        assert len(dropdown) == 1
        assert dropdown[0]["fullName"] == "Active Manager"
    
    def test_tc_2_1_4_2_inactive_manager_not_in_dropdown(self):
        """TC-2.1.4.2: Pasif müşteri sorumlusu dropdown'da görünmemeli"""
        dropdown = self.service.get_dropdown_list()
        
        # Inactive Manager listede olmamalı
        full_names = [item["fullName"] for item in dropdown]
        assert "Inactive Manager" not in full_names
    
    def test_dropdown_format(self):
        """Dropdown listesi format kontrolü"""
        dropdown = self.service.get_dropdown_list()
        
        for item in dropdown:
            assert "id" in item
            assert "fullName" in item
            assert len(item) == 2  # Sadece id ve fullName olmalı


class TestAccountManagerDetail:
    """FR-2.1.5: Müşteri Sorumlusu Detay Görüntüleme Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'i sıfırla"""
        self.service = AccountManagerService()
        self.service.account_managers = []
        self.service.next_id = 1
        
        # Bir manager oluştur
        manager_data = AccountManagerCreate(
            firstName="Test",
            lastName="Manager",
            email="test@crm.com"
        )
        self.service.create_account_manager(manager_data)
    
    def test_tc_2_1_5_1_get_manager_by_valid_id(self):
        """TC-2.1.5.1: Geçerli ID ile müşteri sorumlusu görüntüleme"""
        manager = self.service.get_by_id(1)
        
        assert manager is not None
        assert manager.id == 1
        assert manager.firstName == "Test"
    
    def test_tc_2_1_5_2_get_manager_by_invalid_id(self):
        """TC-2.1.5.2: Geçersiz ID ile müşteri sorumlusu görüntüleme"""
        manager = self.service.get_by_id(9999)
        
        assert manager is None


class TestAccountManagerUpdate:
    """FR-2.1.6: Müşteri Sorumlusu Güncelleme Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'i sıfırla"""
        self.service = AccountManagerService()
        self.service.account_managers = []
        self.service.next_id = 1
        
        # Bir manager oluştur
        manager_data = AccountManagerCreate(
            firstName="Original",
            lastName="Manager",
            email="original@crm.com",
            department="Old Department"
        )
        self.service.create_account_manager(manager_data)
    
    def test_tc_2_1_6_1_successful_account_manager_update(self):
        """TC-2.1.6.1: Başarılı müşteri sorumlusu güncelleme"""
        update_data = AccountManagerUpdate(
            firstName="Updated",
            department="New Department"
        )
        
        manager = self.service.update_account_manager(1, update_data)
        
        assert manager.firstName == "Updated"
        assert manager.department == "New Department"
    
    def test_tc_2_1_6_2_deactivate_account_manager(self):
        """TC-2.1.6.2: Müşteri sorumlusunu pasif yapma"""
        update_data = AccountManagerUpdate(isActive=False)
        
        manager = self.service.update_account_manager(1, update_data)
        
        assert manager.isActive is False
    
    def test_update_nonexistent_manager(self):
        """Var olmayan müşteri sorumlusu güncelleme"""
        update_data = AccountManagerUpdate(firstName="Test")
        
        manager = self.service.update_account_manager(9999, update_data)
        
        assert manager is None
    
    def test_update_email_uniqueness(self):
        """Güncelleme sırasında e-posta benzersizlik kontrolü"""
        # İkinci manager oluştur
        second_manager = AccountManagerCreate(
            firstName="Second",
            lastName="Manager",
            email="second@crm.com"
        )
        self.service.create_account_manager(second_manager)
        
        # İkinci manager'ın e-postasını birincinin e-postasıyla güncellemeye çalış
        update_data = AccountManagerUpdate(email="original@crm.com")
        
        with pytest.raises(ValueError) as exc_info:
            self.service.update_account_manager(2, update_data)
        
        assert "Email already exists" in str(exc_info.value)


class TestAccountManagerDelete:
    """FR-2.1.7: Müşteri Sorumlusu Silme Testleri"""
    
    def setup_method(self):
        """Her test öncesi service'i sıfırla"""
        self.service = AccountManagerService()
        self.service.account_managers = []
        self.service.next_id = 1
        
        # Bir manager oluştur
        manager_data = AccountManagerCreate(
            firstName="ToDelete",
            lastName="Manager",
            email="delete@crm.com"
        )
        self.service.create_account_manager(manager_data)
    
    def test_tc_2_1_7_1_successful_account_manager_delete(self):
        """TC-2.1.7.1: Başarılı müşteri sorumlusu silme"""
        result = self.service.delete_account_manager(1)
        
        assert result is True
        assert self.service.get_by_id(1) is None
    
    def test_tc_2_1_7_2_delete_nonexistent_manager(self):
        """TC-2.1.7.2: Var olmayan müşteri sorumlusu silme"""
        result = self.service.delete_account_manager(9999)
        
        assert result is False


class TestAccountManagerHelperMethods:
    """Account Manager yardımcı metod testleri"""
    
    def setup_method(self):
        """Her test öncesi service'i sıfırla"""
        self.service = AccountManagerService()
        self.service.account_managers = []
        self.service.next_id = 1
        
        # Bir manager oluştur
        manager_data = AccountManagerCreate(
            firstName="Test",
            lastName="Manager",
            email="test@crm.com"
        )
        self.service.create_account_manager(manager_data)
    
    def test_get_by_email(self):
        """E-posta ile müşteri sorumlusu getirme"""
        manager = self.service.get_by_email("test@crm.com")
        
        assert manager is not None
        assert manager.email == "test@crm.com"
    
    def test_get_by_email_not_found(self):
        """Var olmayan e-posta ile müşteri sorumlusu getirme"""
        manager = self.service.get_by_email("notfound@crm.com")
        
        assert manager is None
    
    def test_get_active(self):
        """Sadece aktif müşteri sorumlularını getirme"""
        # Pasif manager ekle
        inactive_manager = AccountManagerCreate(
            firstName="Inactive",
            lastName="Manager",
            email="inactive@crm.com"
        )
        manager = self.service.create_account_manager(inactive_manager)
        self.service.update_account_manager(
            manager.id,
            AccountManagerUpdate(isActive=False)
        )
        
        active_managers = self.service.get_active()
        
        assert len(active_managers) == 1
        assert active_managers[0].isActive is True
