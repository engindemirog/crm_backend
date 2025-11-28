from datetime import datetime
from typing import List, Optional
from app.models.account_manager import AccountManager
from app.schemas.account_manager import AccountManagerCreate, AccountManagerUpdate


class AccountManagerService:
    """Account Manager İşlemleri için Service Katmanı"""
    
    def __init__(self):
        self.account_managers: List[AccountManager] = []
        self.next_id = 1
        self._initialize_fake_data()
    
    def _initialize_fake_data(self):
        """Örnek account manager verileri oluştur"""
        fake_managers = [
            AccountManagerCreate(
                firstName="Zeynep",
                lastName="Aydın",
                email="zeynep.aydin@crm.com",
                phone="0532 111 22 33",
                department="Kurumsal Satış"
            ),
            AccountManagerCreate(
                firstName="Burak",
                lastName="Öztürk",
                email="burak.ozturk@crm.com",
                phone="0533 222 33 44",
                department="Bireysel Satış"
            ),
            AccountManagerCreate(
                firstName="Elif",
                lastName="Yıldız",
                email="elif.yildiz@crm.com",
                phone="0534 333 44 55",
                department="Kurumsal Satış"
            ),
            AccountManagerCreate(
                firstName="Can",
                lastName="Kara",
                email="can.kara@crm.com",
                phone="0535 444 55 66",
                department="Bireysel Satış"
            )
        ]
        
        for manager_data in fake_managers:
            self.create_account_manager(manager_data)
    
    def create_account_manager(self, manager_data: AccountManagerCreate) -> AccountManager:
        """Yeni account manager oluştur"""
        # Email kontrolü
        if self.get_by_email(manager_data.email):
            raise ValueError(f"Email already exists: {manager_data.email}")
        
        now = datetime.now()
        manager = AccountManager(
            id=self.next_id,
            firstName=manager_data.firstName,
            lastName=manager_data.lastName,
            email=manager_data.email,
            phone=manager_data.phone,
            department=manager_data.department,
            isActive=True,
            createdAt=now,
            updatedAt=now
        )
        
        self.account_managers.append(manager)
        self.next_id += 1
        
        return manager
    
    def get_all(self) -> List[AccountManager]:
        """Tüm account manager'ları getir"""
        return self.account_managers
    
    def get_active(self) -> List[AccountManager]:
        """Sadece aktif account manager'ları getir"""
        return [m for m in self.account_managers if m.isActive]
    
    def get_by_id(self, manager_id: int) -> Optional[AccountManager]:
        """ID'ye göre account manager getir"""
        for manager in self.account_managers:
            if manager.id == manager_id:
                return manager
        return None
    
    def get_by_email(self, email: str) -> Optional[AccountManager]:
        """Email'e göre account manager getir"""
        for manager in self.account_managers:
            if manager.email == email:
                return manager
        return None
    
    def update_account_manager(self, manager_id: int, manager_data: AccountManagerUpdate) -> Optional[AccountManager]:
        """Account manager bilgilerini güncelle"""
        manager = self.get_by_id(manager_id)
        if not manager:
            return None
        
        # Email güncelleniyorsa, başka manager'da kullanılmadığından emin ol
        if manager_data.email and manager_data.email != manager.email:
            existing = self.get_by_email(manager_data.email)
            if existing:
                raise ValueError(f"Email already exists: {manager_data.email}")
        
        # Güncelleme işlemi
        update_data = manager_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(manager, field, value)
        
        manager.updatedAt = datetime.now()
        
        return manager
    
    def delete_account_manager(self, manager_id: int) -> bool:
        """Account manager sil"""
        manager = self.get_by_id(manager_id)
        if not manager:
            return False
        
        self.account_managers.remove(manager)
        return True
    
    def get_dropdown_list(self) -> List[dict]:
        """Dropdown için account manager listesi (sadece aktif olanlar)"""
        return [
            {"id": m.id, "fullName": f"{m.firstName} {m.lastName}"}
            for m in self.account_managers if m.isActive
        ]


# Singleton instance
account_manager_service = AccountManagerService()
