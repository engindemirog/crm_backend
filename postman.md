# CRM Backend - Postman Test Senaryoları

Bu döküman, CRM Backend API'sinin Postman ile adım adım test edilmesi için hazırlanmıştır.

---

## Ön Hazırlık

### 1. Sunucuyu Başlatma

```bash
cd c:\selenium_python\crm_backend
python main.py
```

Sunucu başarıyla başladığında:
- URL: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

### 2. Postman Ortam Değişkenleri

Postman'de yeni bir Environment oluşturun ve aşağıdaki değişkenleri ekleyin:

| Variable | Initial Value | Current Value |
|----------|--------------|---------------|
| `base_url` | `http://localhost:8000` | `http://localhost:8000` |
| `admin_token` | | |
| `cc_token` | | |
| `customer_id` | | |
| `manager_id` | | |

---

## Test Akışı

### Adım 1: Sistem Sağlık Kontrolü

#### 1.1 Health Check

**Request:**
```
Method: GET
URL: {{base_url}}/health
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "status": "healthy"
}
```

#### 1.2 Root Endpoint

**Request:**
```
Method: GET
URL: {{base_url}}/
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "message": "Welcome to CRM API",
  "version": "1.0.0",
  "status": "active"
}
```

---

### Adım 2: Authentication - Login İşlemleri

#### 2.1 Admin Login

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/auth/login
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "username": "admin",
  "password": "admin123"
}
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@crm.com",
    "fullName": "System Admin",
    "userType": "admin"
  }
}
```

**Postman Tests Script:**
```javascript
// Response'u parse et
var jsonData = pm.response.json();

// Token'ı environment variable'a kaydet
pm.environment.set("admin_token", jsonData.access_token);

// Test assertions
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has access_token", function () {
    pm.expect(jsonData).to.have.property('access_token');
});

pm.test("User type is admin", function () {
    pm.expect(jsonData.user.userType).to.eql('admin');
});
```

#### 2.2 CC User Login

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/auth/login
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "username": "cc1",
  "password": "cc123"
}
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 3,
    "username": "cc1",
    "email": "cc1@crm.com",
    "fullName": "Ahmet Yılmaz",
    "userType": "cc"
  }
}
```

**Postman Tests Script:**
```javascript
var jsonData = pm.response.json();
pm.environment.set("cc_token", jsonData.access_token);

pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("User type is cc", function () {
    pm.expect(jsonData.user.userType).to.eql('cc');
});
```

#### 2.3 Login - Geçersiz Kimlik Bilgileri

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/auth/login
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "username": "admin",
  "password": "wrongpassword"
}
```

**Beklenen Response:**
```json
Status: 401 Unauthorized
Body:
{
  "detail": "Incorrect username or password"
}
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 401", function () {
    pm.response.to.have.status(401);
});

pm.test("Error message is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.detail).to.include("Incorrect username or password");
});
```

---

### Adım 3: Authentication - Token Doğrulama

#### 3.1 Get Current User (Me) - Geçerli Token

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/auth/me
Headers:
  Authorization: Bearer {{admin_token}}
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "id": 1,
  "username": "admin",
  "email": "admin@crm.com",
  "fullName": "System Admin",
  "userType": "admin"
}
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Username is admin", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.username).to.eql('admin');
});
```

#### 3.2 Get Current User - Token Yok

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/auth/me
Headers:
  (Authorization header yok)
```

**Beklenen Response:**
```json
Status: 403 Forbidden
```

#### 3.3 Validate Token

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/auth/validate
Headers:
  Authorization: Bearer {{admin_token}}
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "id": 1,
  "username": "admin",
  "email": "admin@crm.com",
  "fullName": "System Admin",
  "userType": "admin"
}
```

---

### Adım 4: Authentication - Admin-Only Endpoints

#### 4.1 Get All Users (Admin)

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/auth/users
Headers:
  Authorization: Bearer {{admin_token}}
```

**Beklenen Response:**
```json
Status: 200 OK
Body: [
  {
    "id": 1,
    "username": "admin",
    "email": "admin@crm.com",
    "fullName": "System Admin",
    "userType": "admin"
  },
  {
    "id": 2,
    "username": "manager",
    "email": "manager@crm.com",
    "fullName": "John Manager",
    "userType": "admin"
  },
  ...
]
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Returns array of users", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array');
    pm.expect(jsonData.length).to.eql(5);
});
```

#### 4.2 Get All Users (CC - Forbidden)

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/auth/users
Headers:
  Authorization: Bearer {{cc_token}}
```

**Beklenen Response:**
```json
Status: 403 Forbidden
Body:
{
  "detail": "Admin privileges required"
}
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 403", function () {
    pm.response.to.have.status(403);
});

pm.test("Admin privileges required message", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.detail).to.include("Admin privileges required");
});
```

#### 4.3 Get Users By Type - Admin

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/auth/users/type/admin
Headers:
  Authorization: Bearer {{admin_token}}
```

**Beklenen Response:**
```json
Status: 200 OK
Body: [
  {
    "id": 1,
    "username": "admin",
    "email": "admin@crm.com",
    "fullName": "System Admin",
    "userType": "admin"
  },
  {
    "id": 2,
    "username": "manager",
    "email": "manager@crm.com",
    "fullName": "John Manager",
    "userType": "admin"
  }
]
```

#### 4.4 Get Users By Type - CC

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/auth/users/type/cc
Headers:
  Authorization: Bearer {{admin_token}}
```

**Beklenen Response:**
```json
Status: 200 OK
Body: [
  {
    "id": 3,
    "username": "cc1",
    "email": "cc1@crm.com",
    "fullName": "Ahmet Yılmaz",
    "userType": "cc"
  },
  ...
]
```

---

### Adım 5: Müşteri Sorumlusu (Account Manager) İşlemleri

#### 5.1 Müşteri Sorumlusu Oluşturma

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/account-managers/
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "firstName": "Mehmet",
  "lastName": "Öztürk",
  "email": "mehmet.ozturk@crm.com",
  "phone": "0532 111 22 33",
  "department": "Kurumsal Satış"
}
```

**Beklenen Response:**
```json
Status: 201 Created
Body:
{
  "id": 1,
  "firstName": "Mehmet",
  "lastName": "Öztürk",
  "email": "mehmet.ozturk@crm.com",
  "phone": "0532 111 22 33",
  "department": "Kurumsal Satış",
  "isActive": true,
  "fullName": "Mehmet Öztürk",
  "createdAt": "2025-12-05T...",
  "updatedAt": "2025-12-05T..."
}
```

**Postman Tests Script:**
```javascript
var jsonData = pm.response.json();

// Manager ID'yi kaydet
pm.environment.set("manager_id", jsonData.id);

pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Manager is active by default", function () {
    pm.expect(jsonData.isActive).to.be.true;
});

pm.test("Full name is correct", function () {
    pm.expect(jsonData.fullName).to.eql("Mehmet Öztürk");
});
```

#### 5.2 Müşteri Sorumlusu Oluşturma - Sadece Zorunlu Alanlar

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/account-managers/
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "firstName": "Ayşe",
  "lastName": "Demir",
  "email": "ayse.demir@crm.com"
}
```

**Beklenen Response:**
```json
Status: 201 Created
Body:
{
  "id": 2,
  "firstName": "Ayşe",
  "lastName": "Demir",
  "email": "ayse.demir@crm.com",
  "phone": null,
  "department": null,
  "isActive": true,
  "fullName": "Ayşe Demir",
  "createdAt": "2025-12-05T...",
  "updatedAt": "2025-12-05T..."
}
```

#### 5.3 Müşteri Sorumlusu Listeleme

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/account-managers/
```

**Beklenen Response:**
```json
Status: 200 OK
Body: [
  {
    "id": 1,
    "firstName": "Mehmet",
    "lastName": "Öztürk",
    "email": "mehmet.ozturk@crm.com",
    "phone": "0532 111 22 33",
    "department": "Kurumsal Satış",
    "isActive": true,
    "fullName": "Mehmet Öztürk",
    "createdAt": "2025-12-05T...",
    "updatedAt": "2025-12-05T..."
  },
  ...
]
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Returns array", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array');
});
```

#### 5.4 Müşteri Sorumlusu Dropdown Listesi

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/account-managers/dropdown
```

**Beklenen Response:**
```json
Status: 200 OK
Body: [
  {
    "id": 1,
    "fullName": "Mehmet Öztürk"
  },
  {
    "id": 2,
    "fullName": "Ayşe Demir"
  }
]
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Each item has only id and fullName", function () {
    var jsonData = pm.response.json();
    jsonData.forEach(function(item) {
        pm.expect(Object.keys(item).length).to.eql(2);
        pm.expect(item).to.have.property('id');
        pm.expect(item).to.have.property('fullName');
    });
});
```

#### 5.5 Müşteri Sorumlusu Detay Görüntüleme

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/account-managers/{{manager_id}}
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "id": 1,
  "firstName": "Mehmet",
  "lastName": "Öztürk",
  ...
}
```

#### 5.6 Müşteri Sorumlusu Güncelleme

**Request:**
```
Method: PUT
URL: {{base_url}}/api/v1/account-managers/{{manager_id}}
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "department": "Bireysel Satış",
  "phone": "0532 999 88 77"
}
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "id": 1,
  "firstName": "Mehmet",
  "lastName": "Öztürk",
  "email": "mehmet.ozturk@crm.com",
  "phone": "0532 999 88 77",
  "department": "Bireysel Satış",
  ...
}
```

**Postman Tests Script:**
```javascript
pm.test("Department updated", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.department).to.eql("Bireysel Satış");
});

pm.test("Phone updated", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.phone).to.eql("0532 999 88 77");
});
```

#### 5.7 Müşteri Sorumlusunu Pasif Yapma

**Request:**
```
Method: PUT
URL: {{base_url}}/api/v1/account-managers/{{manager_id}}
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "isActive": false
}
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "id": 1,
  "isActive": false,
  ...
}
```

#### 5.8 Müşteri Sorumlusu Silme

**Request:**
```
Method: DELETE
URL: {{base_url}}/api/v1/account-managers/{{manager_id}}
```

**Beklenen Response:**
```
Status: 204 No Content
Body: (empty)
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 204", function () {
    pm.response.to.have.status(204);
});
```

---

### Adım 6: Bireysel Müşteri İşlemleri

#### 6.1 Müşteri Oluşturma - Tam Bilgiler

**Önkoşul:** Önce bir account manager oluşturun (Adım 5.1)

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/customers/individual/
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "firstName": "Ali",
  "lastName": "Yılmaz",
  "email": "ali.yilmaz@example.com",
  "password": "SecurePass123!",
  "natId": "12345678901",
  "fatherName": "Mehmet",
  "birthDate": "1990-05-15",
  "accountManagerId": 1
}
```

**Beklenen Response:**
```json
Status: 201 Created
Body:
{
  "id": 1,
  "firstName": "Ali",
  "lastName": "Yılmaz",
  "email": "ali.yilmaz@example.com",
  "natId": "12345678901",
  "fatherName": "Mehmet",
  "birthDate": "1990-05-15",
  "accountManagerId": 1,
  "accountManager": {
    "id": 1,
    "fullName": "Mehmet Öztürk"
  },
  "createdAt": "2025-12-05T...",
  "updatedAt": "2025-12-05T..."
}
```

**NOT:** Response'da `password` alanı YOK (güvenlik).

**Postman Tests Script:**
```javascript
var jsonData = pm.response.json();

// Customer ID'yi kaydet
pm.environment.set("customer_id", jsonData.id);

pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Password is not in response", function () {
    pm.expect(jsonData).to.not.have.property('password');
});

pm.test("Account manager info included", function () {
    pm.expect(jsonData.accountManager).to.have.property('id');
    pm.expect(jsonData.accountManager).to.have.property('fullName');
});

pm.test("Email is correct", function () {
    pm.expect(jsonData.email).to.eql("ali.yilmaz@example.com");
});
```

#### 6.2 Müşteri Oluşturma - Account Manager Olmadan

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/customers/individual/
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "firstName": "Fatma",
  "lastName": "Kaya",
  "email": "fatma.kaya@example.com",
  "password": "Pass123!",
  "natId": "98765432109",
  "fatherName": "Ahmet",
  "birthDate": "1985-08-20"
}
```

**Beklenen Response:**
```json
Status: 201 Created
Body:
{
  "id": 2,
  "firstName": "Fatma",
  "lastName": "Kaya",
  "email": "fatma.kaya@example.com",
  "natId": "98765432109",
  "fatherName": "Ahmet",
  "birthDate": "1985-08-20",
  "accountManagerId": null,
  "accountManager": null,
  ...
}
```

#### 6.3 Müşteri Oluşturma - Eksik Zorunlu Alan

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/customers/individual/
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "firstName": "Test",
  "email": "test@example.com"
}
```

**Beklenen Response:**
```json
Status: 422 Unprocessable Entity
Body:
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "lastName"],
      "msg": "Field required",
      ...
    },
    ...
  ]
}
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 422", function () {
    pm.response.to.have.status(422);
});

pm.test("Validation errors present", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('detail');
    pm.expect(jsonData.detail).to.be.an('array');
});
```

#### 6.4 Müşteri Oluşturma - Tekrarlayan E-posta

**Önkoşul:** ali.yilmaz@example.com e-postası ile müşteri mevcut (Adım 6.1)

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/customers/individual/
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "firstName": "Veli",
  "lastName": "Demir",
  "email": "ali.yilmaz@example.com",
  "password": "Pass123!",
  "natId": "11111111111",
  "fatherName": "Ali",
  "birthDate": "1992-03-10"
}
```

**Beklenen Response:**
```json
Status: 400 Bad Request
Body:
{
  "detail": "Email already exists"
}
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Email exists error", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.detail).to.include("Email already exists");
});
```

#### 6.5 Müşteri Oluşturma - Tekrarlayan TC Kimlik No

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/customers/individual/
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "firstName": "Zeynep",
  "lastName": "Arslan",
  "email": "zeynep@example.com",
  "password": "Pass123!",
  "natId": "12345678901",
  "fatherName": "Hasan",
  "birthDate": "1988-11-25"
}
```

**Beklenen Response:**
```json
Status: 400 Bad Request
Body:
{
  "detail": "National ID already exists"
}
```

#### 6.6 Müşteri Oluşturma - Geçersiz Account Manager ID

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/customers/individual/
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "firstName": "Can",
  "lastName": "Yıldız",
  "email": "can@example.com",
  "password": "Pass123!",
  "natId": "22222222222",
  "fatherName": "Kemal",
  "birthDate": "1995-01-01",
  "accountManagerId": 9999
}
```

**Beklenen Response:**
```json
Status: 400 Bad Request
Body:
{
  "detail": "Account Manager not found"
}
```

#### 6.7 Müşteri Oluşturma - Pasif Account Manager

**Önkoşul:** ID=1 olan manager'ı pasif yapın (Adım 5.7)

**Request:**
```
Method: POST
URL: {{base_url}}/api/v1/customers/individual/
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "firstName": "Deniz",
  "lastName": "Kurt",
  "email": "deniz@example.com",
  "password": "Pass123!",
  "natId": "33333333333",
  "fatherName": "Osman",
  "birthDate": "1993-07-12",
  "accountManagerId": 1
}
```

**Beklenen Response:**
```json
Status: 400 Bad Request
Body:
{
  "detail": "Account Manager is not active"
}
```

#### 6.8 Müşteri Listeleme

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/customers/individual/
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "items": [
    {
      "id": 1,
      "firstName": "Ali",
      "lastName": "Yılmaz",
      "email": "ali.yilmaz@example.com",
      "natId": "12345678901",
      "fatherName": "Mehmet",
      "birthDate": "1990-05-15",
      "accountManagerId": 1,
      "accountManager": {
        "id": 1,
        "fullName": "Mehmet Öztürk"
      },
      "createdAt": "2025-12-05T...",
      "updatedAt": "2025-12-05T..."
    },
    ...
  ],
  "total": 2
}
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has items and total", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('items');
    pm.expect(jsonData).to.have.property('total');
});

pm.test("Items is an array", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.items).to.be.an('array');
});

pm.test("Total matches items length", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.total).to.eql(jsonData.items.length);
});
```

#### 6.9 Müşteri Detay Görüntüleme

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/customers/individual/{{customer_id}}
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "id": 1,
  "firstName": "Ali",
  "lastName": "Yılmaz",
  "email": "ali.yilmaz@example.com",
  "natId": "12345678901",
  "fatherName": "Mehmet",
  "birthDate": "1990-05-15",
  "accountManagerId": 1,
  "accountManager": {
    "id": 1,
    "fullName": "Mehmet Öztürk"
  },
  "createdAt": "2025-12-05T...",
  "updatedAt": "2025-12-05T..."
}
```

#### 6.10 Müşteri Detay - Bulunamadı

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/customers/individual/9999
```

**Beklenen Response:**
```json
Status: 404 Not Found
Body:
{
  "detail": "Customer not found"
}
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 404", function () {
    pm.response.to.have.status(404);
});
```

#### 6.11 Müşteri Güncelleme - Tam Güncelleme

**Request:**
```
Method: PUT
URL: {{base_url}}/api/v1/customers/individual/{{customer_id}}
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "firstName": "Ali Updated",
  "lastName": "Yılmaz Updated",
  "email": "ali.updated@example.com",
  "password": "NewPass123!",
  "fatherName": "Mehmet Ali"
}
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "id": 1,
  "firstName": "Ali Updated",
  "lastName": "Yılmaz Updated",
  "email": "ali.updated@example.com",
  "natId": "12345678901",
  "fatherName": "Mehmet Ali",
  "birthDate": "1990-05-15",
  "accountManagerId": 1,
  "accountManager": {
    "id": 1,
    "fullName": "Mehmet Öztürk"
  },
  "createdAt": "2025-12-05T...",
  "updatedAt": "2025-12-05T..."
}
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("First name updated", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.firstName).to.eql("Ali Updated");
});

pm.test("UpdatedAt changed", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.updatedAt).to.not.eql(jsonData.createdAt);
});
```

#### 6.12 Müşteri Güncelleme - Kısmi Güncelleme

**Request:**
```
Method: PUT
URL: {{base_url}}/api/v1/customers/individual/{{customer_id}}
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "phone": "0532 555 66 77"
}
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "id": 1,
  "firstName": "Ali Updated",
  "lastName": "Yılmaz Updated",
  ...
}
```

#### 6.13 Müşteri Güncelleme - Account Manager Değiştirme

**Önkoşul:** ID=2 olan aktif bir manager mevcut

**Request:**
```
Method: PUT
URL: {{base_url}}/api/v1/customers/individual/{{customer_id}}
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "accountManagerId": 2
}
```

**Beklenen Response:**
```json
Status: 200 OK
Body:
{
  "id": 1,
  "accountManagerId": 2,
  "accountManager": {
    "id": 2,
    "fullName": "Ayşe Demir"
  },
  ...
}
```

#### 6.14 Müşteri Silme

**Request:**
```
Method: DELETE
URL: {{base_url}}/api/v1/customers/individual/{{customer_id}}
```

**Beklenen Response:**
```
Status: 204 No Content
Body: (empty)
```

**Postman Tests Script:**
```javascript
pm.test("Status code is 204", function () {
    pm.response.to.have.status(204);
});

pm.test("Response body is empty", function () {
    pm.expect(pm.response.text()).to.eql("");
});
```

#### 6.15 Silinen Müşteriyi Görüntüleme

**Request:**
```
Method: GET
URL: {{base_url}}/api/v1/customers/individual/{{customer_id}}
```

**Beklenen Response:**
```json
Status: 404 Not Found
Body:
{
  "detail": "Customer not found"
}
```

---

### Adım 7: Swagger UI Üzerinden Test

#### 7.1 Swagger UI Erişimi

**Browser'da açın:**
```
http://localhost:8000/docs
```

#### 7.2 Swagger'da Authentication

1. Sağ üstteki "Authorize" butonuna tıklayın
2. Value alanına: `Bearer {admin_token}` yazın
3. "Authorize" butonuna tıklayın
4. "Close" ile kapatın
5. Artık korumalı endpoint'leri test edebilirsiniz

---

## Test Koleksiyonu Oluşturma

### Postman Collection Yapısı

```
CRM Backend API Tests
├── 1. System Health
│   ├── Health Check
│   └── Root Endpoint
├── 2. Authentication
│   ├── Admin Login
│   ├── CC Login
│   ├── Invalid Login
│   ├── Get Me
│   ├── Validate Token
│   ├── Get All Users (Admin)
│   ├── Get All Users (CC - Forbidden)
│   └── Get Users By Type
├── 3. Account Managers
│   ├── Create Manager (Full)
│   ├── Create Manager (Minimal)
│   ├── List Managers
│   ├── Dropdown List
│   ├── Get Manager Detail
│   ├── Update Manager
│   ├── Deactivate Manager
│   └── Delete Manager
└── 4. Customers
    ├── Create Customer (With Manager)
    ├── Create Customer (Without Manager)
    ├── Create Customer (Missing Fields)
    ├── Create Customer (Duplicate Email)
    ├── Create Customer (Duplicate NatId)
    ├── Create Customer (Invalid Manager)
    ├── Create Customer (Inactive Manager)
    ├── List Customers
    ├── Get Customer Detail
    ├── Get Customer (Not Found)
    ├── Update Customer (Full)
    ├── Update Customer (Partial)
    ├── Update Customer (Change Manager)
    ├── Delete Customer
    └── Get Deleted Customer (404)
```

---

## Test Senaryoları Özeti

| Kategori | Test Sayısı |
|----------|-------------|
| Sistem Sağlık | 2 |
| Authentication | 8 |
| Account Managers | 8 |
| Customers | 15 |
| **TOPLAM** | **33** |

---

## Hızlı Test Akışı (Happy Path)

### Sıralı Test Akışı

1. ✅ Health Check
2. ✅ Admin Login (token al)
3. ✅ Create Account Manager
4. ✅ Get Dropdown List
5. ✅ Create Customer (with manager)
6. ✅ List Customers
7. ✅ Get Customer Detail
8. ✅ Update Customer
9. ✅ Delete Customer

Bu akış yaklaşık **2-3 dakika** sürer.

---

## Troubleshooting

### Sorun: "Connection Refused"
**Çözüm:** Sunucunun çalıştığından emin olun (`python main.py`)

### Sorun: "401 Unauthorized"
**Çözüm:** Token'ın doğru gönderildiğinden emin olun
- Header: `Authorization: Bearer {{admin_token}}`

### Sorun: "422 Validation Error"
**Çözüm:** Request body'deki zorunlu alanları kontrol edin

### Sorun: Token süresi doldu
**Çözüm:** Yeniden login olun ve yeni token alın

---

*Son güncelleme: 5 Aralık 2025*
