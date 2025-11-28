# CRM Application - Test Senaryoları

## Doküman Bilgileri
- **Proje Adı:** CRM (Customer Relationship Management) Application
- **Versiyon:** 1.0.0
- **Tarih:** 28 Kasım 2025
- **Referans:** FunctionalRequirements.md

---

## 1. Bireysel Müşteri Yönetimi Test Senaryoları

### 1.1 Bireysel Müşteri Ekleme (FR-1.1.1)

#### TC-1.1.1.1: Başarılı Bireysel Müşteri Ekleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.1.1 |
| **Açıklama** | Tüm zorunlu alanlar doldurularak yeni bireysel müşteri ekleme |
| **Ön Koşul** | Sistem çalışır durumda |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ endpoint'ine istek gönder<br>2. Tüm zorunlu alanları doldur (firstName, lastName, email, password, natId, fatherName, birthDate) |
| **Test Verisi** | `{"firstName": "Test", "lastName": "User", "email": "test@example.com", "password": "123456", "natId": "12345678901", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00"}` |
| **Beklenen Sonuç** | HTTP 201 Created, müşteri kaydı oluşturulur, id, createdAt, updatedAt otomatik atanır |

#### TC-1.1.1.2: Müşteri Sorumlusu ile Bireysel Müşteri Ekleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.1.2 |
| **Açıklama** | Müşteri sorumlusu atanarak yeni bireysel müşteri ekleme |
| **Ön Koşul** | Sistemde aktif bir müşteri sorumlusu (ID: 1) mevcut |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ endpoint'ine istek gönder<br>2. accountManagerId alanını ekle |
| **Test Verisi** | `{"firstName": "Test", "lastName": "User", "email": "test2@example.com", "password": "123456", "natId": "12345678902", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00", "accountManagerId": 1}` |
| **Beklenen Sonuç** | HTTP 201 Created, müşteri kaydı oluşturulur, accountManager bilgisi response'da yer alır |

#### TC-1.1.1.3: Eksik Zorunlu Alan ile Müşteri Ekleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.1.3 |
| **Açıklama** | firstName alanı olmadan müşteri ekleme denemesi |
| **Ön Koşul** | - |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ endpoint'ine istek gönder<br>2. firstName alanını gönderme |
| **Test Verisi** | `{"lastName": "User", "email": "test@example.com", "password": "123456", "natId": "12345678901", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00"}` |
| **Beklenen Sonuç** | HTTP 422 Unprocessable Entity, validasyon hatası döner |

#### TC-1.1.1.4: Kısa Ad ile Müşteri Ekleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.1.4 |
| **Açıklama** | 2 karakterden kısa ad ile müşteri ekleme denemesi |
| **Ön Koşul** | - |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ endpoint'ine istek gönder<br>2. firstName alanını "A" olarak gönder |
| **Test Verisi** | `{"firstName": "A", "lastName": "User", "email": "test@example.com", "password": "123456", "natId": "12345678901", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00"}` |
| **Beklenen Sonuç** | HTTP 422 Unprocessable Entity, minimum uzunluk hatası döner |

#### TC-1.1.1.5: Kısa Şifre ile Müşteri Ekleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.1.5 |
| **Açıklama** | 6 karakterden kısa şifre ile müşteri ekleme denemesi |
| **Ön Koşul** | - |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ endpoint'ine istek gönder<br>2. password alanını "12345" olarak gönder |
| **Test Verisi** | `{"firstName": "Test", "lastName": "User", "email": "test@example.com", "password": "12345", "natId": "12345678901", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00"}` |
| **Beklenen Sonuç** | HTTP 422 Unprocessable Entity, minimum uzunluk hatası döner |

#### TC-1.1.1.6: Geçersiz TC Kimlik No Formatı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.1.6 |
| **Açıklama** | 11 haneden farklı TC Kimlik No ile müşteri ekleme denemesi |
| **Ön Koşul** | - |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ endpoint'ine istek gönder<br>2. natId alanını "123456" olarak gönder |
| **Test Verisi** | `{"firstName": "Test", "lastName": "User", "email": "test@example.com", "password": "123456", "natId": "123456", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00"}` |
| **Beklenen Sonuç** | HTTP 422 Unprocessable Entity, TC Kimlik No format hatası döner |

#### TC-1.1.1.7: Harfli TC Kimlik No
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.1.7 |
| **Açıklama** | Harf içeren TC Kimlik No ile müşteri ekleme denemesi |
| **Ön Koşul** | - |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ endpoint'ine istek gönder<br>2. natId alanını "1234567890A" olarak gönder |
| **Test Verisi** | `{"firstName": "Test", "lastName": "User", "email": "test@example.com", "password": "123456", "natId": "1234567890A", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00"}` |
| **Beklenen Sonuç** | HTTP 422 Unprocessable Entity, TC Kimlik No format hatası döner |

#### TC-1.1.1.8: Geçersiz E-posta Formatı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.1.8 |
| **Açıklama** | Geçersiz e-posta formatı ile müşteri ekleme denemesi |
| **Ön Koşul** | - |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ endpoint'ine istek gönder<br>2. email alanını "invalid-email" olarak gönder |
| **Test Verisi** | `{"firstName": "Test", "lastName": "User", "email": "invalid-email", "password": "123456", "natId": "12345678901", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00"}` |
| **Beklenen Sonuç** | HTTP 422 Unprocessable Entity, e-posta format hatası döner |

---

### 1.2 E-posta Benzersizlik Kontrolü (FR-1.1.2)

#### TC-1.1.2.1: Mevcut E-posta ile Müşteri Ekleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.2.1 |
| **Açıklama** | Sistemde kayıtlı e-posta adresi ile yeni müşteri ekleme denemesi |
| **Ön Koşul** | "ahmet.yilmaz@example.com" e-postası ile bir müşteri sistemde kayıtlı |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ endpoint'ine istek gönder<br>2. Mevcut e-posta adresini kullan |
| **Test Verisi** | `{"firstName": "Yeni", "lastName": "Kullanici", "email": "ahmet.yilmaz@example.com", "password": "123456", "natId": "99999999999", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00"}` |
| **Beklenen Sonuç** | HTTP 400 Bad Request, "Email already exists" hatası döner |

#### TC-1.1.2.2: Güncelleme ile Mevcut E-posta Atama
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.2.2 |
| **Açıklama** | Müşteri güncellemesinde başka müşteriye ait e-posta kullanma denemesi |
| **Ön Koşul** | ID:1 ve ID:2 müşterileri mevcut, ID:2'nin e-postası "ayse.demir@example.com" |
| **Test Adımları** | 1. PUT /api/v1/customers/individual/1 endpoint'ine istek gönder<br>2. email alanını "ayse.demir@example.com" olarak gönder |
| **Test Verisi** | `{"email": "ayse.demir@example.com"}` |
| **Beklenen Sonuç** | HTTP 400 Bad Request, "Email already exists" hatası döner |

---

### 1.3 TC Kimlik No Benzersizlik Kontrolü (FR-1.1.3)

#### TC-1.1.3.1: Mevcut TC Kimlik No ile Müşteri Ekleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.3.1 |
| **Açıklama** | Sistemde kayıtlı TC Kimlik No ile yeni müşteri ekleme denemesi |
| **Ön Koşul** | "12345678901" TC Kimlik No ile bir müşteri sistemde kayıtlı |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ endpoint'ine istek gönder<br>2. Mevcut TC Kimlik No'yu kullan |
| **Test Verisi** | `{"firstName": "Yeni", "lastName": "Kullanici", "email": "yeni@example.com", "password": "123456", "natId": "12345678901", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00"}` |
| **Beklenen Sonuç** | HTTP 400 Bad Request, "National ID already exists" hatası döner |

#### TC-1.1.3.2: Güncelleme ile Mevcut TC Kimlik No Atama
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.3.2 |
| **Açıklama** | Müşteri güncellemesinde başka müşteriye ait TC Kimlik No kullanma denemesi |
| **Ön Koşul** | ID:1 ve ID:2 müşterileri mevcut, ID:2'nin natId'si "98765432109" |
| **Test Adımları** | 1. PUT /api/v1/customers/individual/1 endpoint'ine istek gönder<br>2. natId alanını "98765432109" olarak gönder |
| **Test Verisi** | `{"natId": "98765432109"}` |
| **Beklenen Sonuç** | HTTP 400 Bad Request, "National ID already exists" hatası döner |

---

### 1.4 Şifre Güvenliği (FR-1.1.4)

#### TC-1.1.4.1: Şifre Hashleme Kontrolü
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.4.1 |
| **Açıklama** | Oluşturulan müşterinin şifresinin hashlenmiş olduğunun kontrolü |
| **Ön Koşul** | - |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ ile yeni müşteri oluştur<br>2. Sistemde saklanan şifre değerini kontrol et |
| **Test Verisi** | `{"firstName": "Test", "lastName": "User", "email": "hash@example.com", "password": "123456", "natId": "55555555555", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00"}` |
| **Beklenen Sonuç** | Saklanan şifre "123456" değil, bcrypt hash formatında olmalı (örn: $2b$12$...) |

---

### 1.5 Bireysel Müşteri Listeleme (FR-1.1.5)

#### TC-1.1.5.1: Tüm Müşterileri Listeleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.5.1 |
| **Açıklama** | Sistemdeki tüm bireysel müşterilerin listelenmesi |
| **Ön Koşul** | Sistemde en az 1 müşteri kayıtlı |
| **Test Adımları** | 1. GET /api/v1/customers/individual/ endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, response'da "total" ve "customers" alanları bulunur, her müşteride accountManager bilgisi yer alır |

#### TC-1.1.5.2: Boş Müşteri Listesi
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.5.2 |
| **Açıklama** | Sistemde müşteri yokken listeleme |
| **Ön Koşul** | Sistemde hiç müşteri yok |
| **Test Adımları** | 1. GET /api/v1/customers/individual/ endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, `{"total": 0, "customers": []}` döner |

---

### 1.6 Bireysel Müşteri Detay Görüntüleme (FR-1.1.6)

#### TC-1.1.6.1: Geçerli ID ile Müşteri Görüntüleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.6.1 |
| **Açıklama** | Mevcut bir müşterinin detaylarını görüntüleme |
| **Ön Koşul** | ID:1 müşterisi sistemde kayıtlı |
| **Test Adımları** | 1. GET /api/v1/customers/individual/1 endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, müşteri detayları ve accountManager bilgisi döner |

#### TC-1.1.6.2: Geçersiz ID ile Müşteri Görüntüleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.6.2 |
| **Açıklama** | Var olmayan müşteri ID'si ile görüntüleme denemesi |
| **Ön Koşul** | ID:9999 müşterisi sistemde yok |
| **Test Adımları** | 1. GET /api/v1/customers/individual/9999 endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 404 Not Found, "Customer with ID 9999 not found" hatası döner |

---

### 1.7 Bireysel Müşteri Güncelleme (FR-1.1.7)

#### TC-1.1.7.1: Başarılı Müşteri Güncelleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.7.1 |
| **Açıklama** | Müşteri ad ve soyad güncelleme |
| **Ön Koşul** | ID:1 müşterisi sistemde kayıtlı |
| **Test Adımları** | 1. PUT /api/v1/customers/individual/1 endpoint'ine istek gönder<br>2. firstName ve lastName alanlarını gönder |
| **Test Verisi** | `{"firstName": "Yeni Ad", "lastName": "Yeni Soyad"}` |
| **Beklenen Sonuç** | HTTP 200 OK, müşteri bilgileri güncellenir, updatedAt yenilenir |

#### TC-1.1.7.2: Kısmi Güncelleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.7.2 |
| **Açıklama** | Sadece tek alan güncelleme (diğer alanlar değişmemeli) |
| **Ön Koşul** | ID:1 müşterisi sistemde kayıtlı |
| **Test Adımları** | 1. Mevcut müşteri bilgilerini kaydet<br>2. PUT /api/v1/customers/individual/1 ile sadece firstName gönder<br>3. Diğer alanların değişmediğini kontrol et |
| **Test Verisi** | `{"firstName": "Sadece Ad"}` |
| **Beklenen Sonuç** | HTTP 200 OK, sadece firstName güncellenir, diğer alanlar aynı kalır |

#### TC-1.1.7.3: Müşteri Sorumlusu Güncelleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.7.3 |
| **Açıklama** | Müşteriye yeni müşteri sorumlusu atama |
| **Ön Koşul** | ID:1 müşterisi ve ID:2 aktif müşteri sorumlusu mevcut |
| **Test Adımları** | 1. PUT /api/v1/customers/individual/1 endpoint'ine istek gönder<br>2. accountManagerId alanını gönder |
| **Test Verisi** | `{"accountManagerId": 2}` |
| **Beklenen Sonuç** | HTTP 200 OK, müşteri sorumlusu güncellenir, response'da yeni accountManager bilgisi yer alır |

#### TC-1.1.7.4: Var Olmayan Müşteri Güncelleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.7.4 |
| **Açıklama** | Var olmayan müşteri ID'si ile güncelleme denemesi |
| **Ön Koşul** | ID:9999 müşterisi sistemde yok |
| **Test Adımları** | 1. PUT /api/v1/customers/individual/9999 endpoint'ine istek gönder |
| **Test Verisi** | `{"firstName": "Test"}` |
| **Beklenen Sonuç** | HTTP 404 Not Found hatası döner |

---

### 1.8 Bireysel Müşteri Silme (FR-1.1.8)

#### TC-1.1.8.1: Başarılı Müşteri Silme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.8.1 |
| **Açıklama** | Mevcut müşteriyi silme |
| **Ön Koşul** | ID:1 müşterisi sistemde kayıtlı |
| **Test Adımları** | 1. DELETE /api/v1/customers/individual/1 endpoint'ine istek gönder<br>2. GET /api/v1/customers/individual/1 ile silindi mi kontrol et |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 204 No Content, müşteri sistemden silinir |

#### TC-1.1.8.2: Var Olmayan Müşteri Silme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-1.1.8.2 |
| **Açıklama** | Var olmayan müşteri ID'si ile silme denemesi |
| **Ön Koşul** | ID:9999 müşterisi sistemde yok |
| **Test Adımları** | 1. DELETE /api/v1/customers/individual/9999 endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 404 Not Found hatası döner |

---

## 2. Müşteri Sorumlusu (Account Manager) Test Senaryoları

### 2.1 Müşteri Sorumlusu Ekleme (FR-2.1.1)

#### TC-2.1.1.1: Başarılı Müşteri Sorumlusu Ekleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.1.1 |
| **Açıklama** | Tüm zorunlu alanlar ile yeni müşteri sorumlusu ekleme |
| **Ön Koşul** | - |
| **Test Adımları** | 1. POST /api/v1/account-managers/ endpoint'ine istek gönder |
| **Test Verisi** | `{"firstName": "Yeni", "lastName": "Manager", "email": "manager@crm.com"}` |
| **Beklenen Sonuç** | HTTP 201 Created, müşteri sorumlusu oluşturulur, isActive: true, fullName oluşturulur |

#### TC-2.1.1.2: Opsiyonel Alanlar ile Müşteri Sorumlusu Ekleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.1.2 |
| **Açıklama** | Tüm alanlar doldurularak müşteri sorumlusu ekleme |
| **Ön Koşul** | - |
| **Test Adımları** | 1. POST /api/v1/account-managers/ endpoint'ine istek gönder<br>2. phone ve department alanlarını ekle |
| **Test Verisi** | `{"firstName": "Tam", "lastName": "Manager", "email": "tam@crm.com", "phone": "0532 123 45 67", "department": "Kurumsal Satış"}` |
| **Beklenen Sonuç** | HTTP 201 Created, tüm alanlar kaydedilir |

#### TC-2.1.1.3: Geçersiz E-posta ile Müşteri Sorumlusu Ekleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.1.3 |
| **Açıklama** | Geçersiz e-posta formatı ile ekleme denemesi |
| **Ön Koşul** | - |
| **Test Adımları** | 1. POST /api/v1/account-managers/ endpoint'ine istek gönder |
| **Test Verisi** | `{"firstName": "Test", "lastName": "Manager", "email": "invalid-email"}` |
| **Beklenen Sonuç** | HTTP 422 Unprocessable Entity, e-posta format hatası döner |

---

### 2.2 E-posta Benzersizlik Kontrolü (FR-2.1.2)

#### TC-2.1.2.1: Mevcut E-posta ile Müşteri Sorumlusu Ekleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.2.1 |
| **Açıklama** | Sistemde kayıtlı e-posta ile yeni müşteri sorumlusu ekleme denemesi |
| **Ön Koşul** | "zeynep.aydin@crm.com" e-postası ile müşteri sorumlusu mevcut |
| **Test Adımları** | 1. POST /api/v1/account-managers/ endpoint'ine istek gönder |
| **Test Verisi** | `{"firstName": "Yeni", "lastName": "Kişi", "email": "zeynep.aydin@crm.com"}` |
| **Beklenen Sonuç** | HTTP 400 Bad Request, "Email already exists" hatası döner |

---

### 2.3 Müşteri Sorumlusu Listeleme (FR-2.1.3)

#### TC-2.1.3.1: Tüm Müşteri Sorumlularını Listeleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.3.1 |
| **Açıklama** | Sistemdeki tüm müşteri sorumlularının listelenmesi |
| **Ön Koşul** | Sistemde en az 1 müşteri sorumlusu kayıtlı |
| **Test Adımları** | 1. GET /api/v1/account-managers/ endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, response'da "total" ve "accountManagers" alanları bulunur, her kayıtta fullName yer alır |

---

### 2.4 Müşteri Sorumlusu Dropdown Listesi (FR-2.1.4)

#### TC-2.1.4.1: Dropdown için Aktif Müşteri Sorumluları
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.4.1 |
| **Açıklama** | Sadece aktif müşteri sorumlularının dropdown için listelenmesi |
| **Ön Koşul** | Sistemde aktif ve pasif müşteri sorumluları mevcut |
| **Test Adımları** | 1. GET /api/v1/account-managers/dropdown endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, sadece aktif olanlar listelenir, her kayıtta sadece id ve fullName bulunur |

#### TC-2.1.4.2: Pasif Müşteri Sorumlusu Dropdown'da Görünmemeli
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.4.2 |
| **Açıklama** | Pasif müşteri sorumlusunun dropdown listesinde olmaması |
| **Ön Koşul** | ID:1 müşteri sorumlusu pasif (isActive: false) yapılmış |
| **Test Adımları** | 1. PUT /api/v1/account-managers/1 ile isActive: false yap<br>2. GET /api/v1/account-managers/dropdown isteği gönder<br>3. ID:1'in listede olmadığını kontrol et |
| **Test Verisi** | - |
| **Beklenen Sonuç** | ID:1 dropdown listesinde yer almaz |

---

### 2.5 Müşteri Sorumlusu Detay Görüntüleme (FR-2.1.5)

#### TC-2.1.5.1: Geçerli ID ile Müşteri Sorumlusu Görüntüleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.5.1 |
| **Açıklama** | Mevcut müşteri sorumlusunun detaylarını görüntüleme |
| **Ön Koşul** | ID:1 müşteri sorumlusu sistemde kayıtlı |
| **Test Adımları** | 1. GET /api/v1/account-managers/1 endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, müşteri sorumlusu detayları ve fullName döner |

#### TC-2.1.5.2: Geçersiz ID ile Müşteri Sorumlusu Görüntüleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.5.2 |
| **Açıklama** | Var olmayan müşteri sorumlusu ID'si ile görüntüleme |
| **Ön Koşul** | ID:9999 müşteri sorumlusu sistemde yok |
| **Test Adımları** | 1. GET /api/v1/account-managers/9999 endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 404 Not Found hatası döner |

---

### 2.6 Müşteri Sorumlusu Güncelleme (FR-2.1.6)

#### TC-2.1.6.1: Başarılı Müşteri Sorumlusu Güncelleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.6.1 |
| **Açıklama** | Müşteri sorumlusu bilgilerini güncelleme |
| **Ön Koşul** | ID:1 müşteri sorumlusu sistemde kayıtlı |
| **Test Adımları** | 1. PUT /api/v1/account-managers/1 endpoint'ine istek gönder |
| **Test Verisi** | `{"firstName": "Güncel Ad", "department": "Yeni Departman"}` |
| **Beklenen Sonuç** | HTTP 200 OK, bilgiler güncellenir, updatedAt yenilenir |

#### TC-2.1.6.2: Müşteri Sorumlusu Pasif Yapma
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.6.2 |
| **Açıklama** | Müşteri sorumlusunu pasif duruma getirme |
| **Ön Koşul** | ID:1 müşteri sorumlusu aktif durumda |
| **Test Adımları** | 1. PUT /api/v1/account-managers/1 endpoint'ine istek gönder |
| **Test Verisi** | `{"isActive": false}` |
| **Beklenen Sonuç** | HTTP 200 OK, isActive: false olarak güncellenir |

---

### 2.7 Müşteri Sorumlusu Silme (FR-2.1.7)

#### TC-2.1.7.1: Başarılı Müşteri Sorumlusu Silme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.7.1 |
| **Açıklama** | Mevcut müşteri sorumlusunu silme |
| **Ön Koşul** | ID:4 müşteri sorumlusu sistemde kayıtlı |
| **Test Adımları** | 1. DELETE /api/v1/account-managers/4 endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 204 No Content |

#### TC-2.1.7.2: Var Olmayan Müşteri Sorumlusu Silme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-2.1.7.2 |
| **Açıklama** | Var olmayan müşteri sorumlusu silme denemesi |
| **Ön Koşul** | ID:9999 müşteri sorumlusu sistemde yok |
| **Test Adımları** | 1. DELETE /api/v1/account-managers/9999 endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 404 Not Found hatası döner |

---

## 3. Müşteri - Müşteri Sorumlusu İlişkisi Test Senaryoları

### 3.1 Müşteri Sorumlusu Atama (FR-3.1)

#### TC-3.1.1: Geçersiz Müşteri Sorumlusu ID'si ile Atama
| Alan | Değer |
|------|-------|
| **Test ID** | TC-3.1.1 |
| **Açıklama** | Var olmayan müşteri sorumlusu ID'si ile müşteri oluşturma |
| **Ön Koşul** | ID:9999 müşteri sorumlusu sistemde yok |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ endpoint'ine istek gönder<br>2. accountManagerId: 9999 gönder |
| **Test Verisi** | `{"firstName": "Test", "lastName": "User", "email": "test99@example.com", "password": "123456", "natId": "99999999991", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00", "accountManagerId": 9999}` |
| **Beklenen Sonuç** | HTTP 400 Bad Request, "Account Manager with ID 9999 not found" hatası döner |

#### TC-3.1.2: Pasif Müşteri Sorumlusu ile Atama
| Alan | Değer |
|------|-------|
| **Test ID** | TC-3.1.2 |
| **Açıklama** | Pasif müşteri sorumlusu ile müşteri oluşturma denemesi |
| **Ön Koşul** | ID:1 müşteri sorumlusu pasif (isActive: false) durumda |
| **Test Adımları** | 1. ID:1 müşteri sorumlusunu pasif yap<br>2. POST /api/v1/customers/individual/ ile accountManagerId: 1 gönder |
| **Test Verisi** | `{"firstName": "Test", "lastName": "User", "email": "test98@example.com", "password": "123456", "natId": "99999999992", "fatherName": "Father", "birthDate": "1990-01-01T00:00:00", "accountManagerId": 1}` |
| **Beklenen Sonuç** | HTTP 400 Bad Request, "Account Manager with ID 1 is not active" hatası döner |

---

### 3.2 Müşteri Sorumlusu Bilgisi Görüntüleme (FR-3.2)

#### TC-3.2.1: Atanmış Müşteri Sorumlusu Görüntüleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-3.2.1 |
| **Açıklama** | Müşteri sorumlusu atanmış müşterinin detayında accountManager bilgisi |
| **Ön Koşul** | ID:1 müşterisine ID:1 müşteri sorumlusu atanmış |
| **Test Adımları** | 1. GET /api/v1/customers/individual/1 endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, response'da accountManager: {id, fullName} bilgisi yer alır |

#### TC-3.2.2: Atanmamış Müşteri Sorumlusu Görüntüleme
| Alan | Değer |
|------|-------|
| **Test ID** | TC-3.2.2 |
| **Açıklama** | Müşteri sorumlusu atanmamış müşterinin detayı |
| **Ön Koşul** | Müşteri sorumlusu atanmamış bir müşteri mevcut |
| **Test Adımları** | 1. Müşteri sorumlusu olmadan müşteri oluştur<br>2. GET ile müşteri detayını getir |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, response'da accountManager: null döner |

---

## 4. API ve Sistem Test Senaryoları

### 4.1 RESTful API (FR-4.1)

#### TC-4.1.1: API Versiyon Kontrolü
| Alan | Değer |
|------|-------|
| **Test ID** | TC-4.1.1 |
| **Açıklama** | API'nin v1 versiyonuyla çalıştığının kontrolü |
| **Ön Koşul** | - |
| **Test Adımları** | 1. /api/v1/customers/individual/ endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, endpoint v1 versiyonuyla çalışır |

---

### 4.2 API Dokümantasyonu (FR-4.2)

#### TC-4.2.1: Swagger UI Erişimi
| Alan | Değer |
|------|-------|
| **Test ID** | TC-4.2.1 |
| **Açıklama** | Swagger UI dokümantasyonuna erişim |
| **Ön Koşul** | Uygulama çalışır durumda |
| **Test Adımları** | 1. GET /docs endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, Swagger UI sayfası yüklenir |

#### TC-4.2.2: ReDoc Erişimi
| Alan | Değer |
|------|-------|
| **Test ID** | TC-4.2.2 |
| **Açıklama** | ReDoc dokümantasyonuna erişim |
| **Ön Koşul** | Uygulama çalışır durumda |
| **Test Adımları** | 1. GET /redoc endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, ReDoc sayfası yüklenir |

#### TC-4.2.3: OpenAPI JSON Erişimi
| Alan | Değer |
|------|-------|
| **Test ID** | TC-4.2.3 |
| **Açıklama** | OpenAPI JSON spesifikasyonuna erişim |
| **Ön Koşul** | Uygulama çalışır durumda |
| **Test Adımları** | 1. GET /openapi.json endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, JSON formatında OpenAPI spesifikasyonu döner |

---

### 4.3 Sağlık Kontrolü (FR-4.3)

#### TC-4.3.1: Health Check
| Alan | Değer |
|------|-------|
| **Test ID** | TC-4.3.1 |
| **Açıklama** | Sistem sağlık kontrolü |
| **Ön Koşul** | Uygulama çalışır durumda |
| **Test Adımları** | 1. GET /health endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, `{"status": "healthy"}` döner |

---

### 4.4 CORS Desteği (FR-4.4)

#### TC-4.4.1: CORS Preflight Request
| Alan | Değer |
|------|-------|
| **Test ID** | TC-4.4.1 |
| **Açıklama** | CORS preflight isteğinin başarılı olması |
| **Ön Koşul** | - |
| **Test Adımları** | 1. OPTIONS /api/v1/customers/individual/ isteği gönder<br>2. Origin header'ı ekle |
| **Test Verisi** | Headers: `Origin: http://localhost:3000` |
| **Beklenen Sonuç** | HTTP 200 OK, Access-Control-Allow-Origin header'ı döner |

---

### 4.5 Validasyon (FR-4.5)

#### TC-4.5.1: Geçersiz JSON Format
| Alan | Değer |
|------|-------|
| **Test ID** | TC-4.5.1 |
| **Açıklama** | Geçersiz JSON formatında istek gönderme |
| **Ön Koşul** | - |
| **Test Adımları** | 1. POST /api/v1/customers/individual/ endpoint'ine geçersiz JSON gönder |
| **Test Verisi** | `{invalid json}` |
| **Beklenen Sonuç** | HTTP 422 Unprocessable Entity, JSON parse hatası döner |

#### TC-4.5.2: Root Endpoint Erişimi
| Alan | Değer |
|------|-------|
| **Test ID** | TC-4.5.2 |
| **Açıklama** | Ana endpoint'e erişim |
| **Ön Koşul** | - |
| **Test Adımları** | 1. GET / endpoint'ine istek gönder |
| **Test Verisi** | - |
| **Beklenen Sonuç** | HTTP 200 OK, API bilgisi ve versiyon döner |

---

## Test Senaryosu Özeti

| Modül | Toplam Test | Pozitif | Negatif |
|-------|-------------|---------|---------|
| Bireysel Müşteri Yönetimi | 20 | 8 | 12 |
| Müşteri Sorumlusu Yönetimi | 12 | 6 | 6 |
| Müşteri-Sorumlu İlişkisi | 4 | 2 | 2 |
| API ve Sistem | 8 | 7 | 1 |
| **TOPLAM** | **44** | **23** | **21** |
