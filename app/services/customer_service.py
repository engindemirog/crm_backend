from datetime import datetime
from typing import List, Optional
from app.models.customer import IndividualCustomer
from app.schemas.customer import IndividualCustomerCreate, IndividualCustomerUpdate
from app.services.account_manager_service import account_manager_service
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class IndividualCustomerService:
    """Bireysel Müşteri İşlemleri için Service Katmanı"""
    
    def __init__(self):
        self.customers: List[IndividualCustomer] = []
        self.next_id = 1
        self._initialize_fake_data()
    
    def _hash_password(self, password: str) -> str:
        """Şifreyi hashle"""
        return pwd_context.hash(password)
    
    def _initialize_fake_data(self):
        """Örnek müşteri verileri oluştur"""
        fake_customers = [
            IndividualCustomerCreate(
                firstName="Ahmet",
                lastName="Yılmaz",
                email="ahmet.yilmaz@example.com",
                password="password123",
                natId="12345678901",
                fatherName="Mehmet",
                birthDate=datetime(1990, 5, 15),
                accountManagerId=1  # Zeynep Aydın
            ),
            IndividualCustomerCreate(
                firstName="Ayşe",
                lastName="Demir",
                email="ayse.demir@example.com",
                password="password123",
                natId="98765432109",
                fatherName="Ali",
                birthDate=datetime(1985, 8, 22),
                accountManagerId=2  # Burak Öztürk
            ),
            IndividualCustomerCreate(
                firstName="Mehmet",
                lastName="Kaya",
                email="mehmet.kaya@example.com",
                password="password123",
                natId="11122233344",
                fatherName="Hasan",
                birthDate=datetime(1992, 3, 10),
                accountManagerId=1  # Zeynep Aydın
            )
        ]
        
        for customer_data in fake_customers:
            self.create_customer(customer_data)
    
    def create_customer(self, customer_data: IndividualCustomerCreate) -> IndividualCustomer:
        """Yeni müşteri oluştur"""
        # Email kontrolü
        if self.get_customer_by_email(customer_data.email):
            raise ValueError(f"Email already exists: {customer_data.email}")
        
        # TC Kimlik No kontrolü
        if self.get_customer_by_nat_id(customer_data.natId):
            raise ValueError(f"National ID already exists: {customer_data.natId}")
        
        # Account Manager kontrolü
        if customer_data.accountManagerId:
            manager = account_manager_service.get_by_id(customer_data.accountManagerId)
            if not manager:
                raise ValueError(f"Account Manager with ID {customer_data.accountManagerId} not found")
            if not manager.isActive:
                raise ValueError(f"Account Manager with ID {customer_data.accountManagerId} is not active")
        
        now = datetime.now()
        customer = IndividualCustomer(
            id=self.next_id,
            firstName=customer_data.firstName,
            lastName=customer_data.lastName,
            email=customer_data.email,
            password=self._hash_password(customer_data.password),
            natId=customer_data.natId,
            fatherName=customer_data.fatherName,
            birthDate=customer_data.birthDate,
            accountManagerId=customer_data.accountManagerId,
            createdAt=now,
            updatedAt=now
        )
        
        self.customers.append(customer)
        self.next_id += 1
        
        return customer
    
    def get_all_customers(self) -> List[IndividualCustomer]:
        """Tüm müşterileri getir"""
        return self.customers
    
    def get_customer_by_id(self, customer_id: int) -> Optional[IndividualCustomer]:
        """ID'ye göre müşteri getir"""
        for customer in self.customers:
            if customer.id == customer_id:
                return customer
        return None
    
    def get_customer_by_email(self, email: str) -> Optional[IndividualCustomer]:
        """Email'e göre müşteri getir"""
        for customer in self.customers:
            if customer.email == email:
                return customer
        return None
    
    def get_customer_by_nat_id(self, nat_id: str) -> Optional[IndividualCustomer]:
        """TC Kimlik No'ya göre müşteri getir"""
        for customer in self.customers:
            if customer.natId == nat_id:
                return customer
        return None
    
    def update_customer(self, customer_id: int, customer_data: IndividualCustomerUpdate) -> Optional[IndividualCustomer]:
        """Müşteri bilgilerini güncelle"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return None
        
        # Email güncelleniyorsa, başka müşteride kullanılmadığından emin ol
        if customer_data.email and customer_data.email != customer.email:
            existing = self.get_customer_by_email(customer_data.email)
            if existing:
                raise ValueError(f"Email already exists: {customer_data.email}")
        
        # TC Kimlik No güncelleniyorsa, başka müşteride kullanılmadığından emin ol
        if customer_data.natId and customer_data.natId != customer.natId:
            existing = self.get_customer_by_nat_id(customer_data.natId)
            if existing:
                raise ValueError(f"National ID already exists: {customer_data.natId}")
        
        # Account Manager güncelleniyorsa kontrol et
        if customer_data.accountManagerId is not None:
            manager = account_manager_service.get_by_id(customer_data.accountManagerId)
            if not manager:
                raise ValueError(f"Account Manager with ID {customer_data.accountManagerId} not found")
            if not manager.isActive:
                raise ValueError(f"Account Manager with ID {customer_data.accountManagerId} is not active")
        
        # Güncelleme işlemi
        update_data = customer_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "password":
                setattr(customer, field, self._hash_password(value))
            else:
                setattr(customer, field, value)
        
        customer.updatedAt = datetime.now()
        
        return customer
    
    def delete_customer(self, customer_id: int) -> bool:
        """Müşteri sil"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return False
        
        self.customers.remove(customer)
        return True
    
    def get_customer_response(self, customer: IndividualCustomer) -> dict:
        """Müşteri response'u account manager bilgisiyle birlikte döner"""
        response = customer.model_dump()
        
        # Account Manager bilgisini ekle
        if customer.accountManagerId:
            manager = account_manager_service.get_by_id(customer.accountManagerId)
            if manager:
                response["accountManager"] = {
                    "id": manager.id,
                    "fullName": f"{manager.firstName} {manager.lastName}"
                }
            else:
                response["accountManager"] = None
        else:
            response["accountManager"] = None
        
        return response


# Singleton instance
individual_customer_service = IndividualCustomerService()
