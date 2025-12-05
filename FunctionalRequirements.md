# CRM Application - Fonksiyonel Gereksinimler

## Doküman Bilgileri
- **Proje Adı:** CRM (Customer Relationship Management) Application
- **Versiyon:** 1.1.0
- **Tarih:** 5 Aralık 2025
- **Güncelleme:** Authentication modülü eklendi

---

## 1. Müşteri Yönetimi

### 1.1 Bireysel Müşteri Yönetimi

#### FR-1.1.1 Bireysel Müşteri Ekleme
- Sistem, yeni bireysel müşteri kaydı oluşturabilmelidir.
- Müşteri kaydı için aşağıdaki bilgiler zorunludur:
  - Ad (firstName): Minimum 2, maksimum 50 karakter
  - Soyad (lastName): Minimum 2, maksimum 50 karakter
  - E-posta (email): Geçerli e-posta formatında olmalıdır
  - Şifre (password): Minimum 6, maksimum 100 karakter
  - TC Kimlik No (natId): Tam olarak 11 haneli rakamlardan oluşmalıdır
  - Baba Adı (fatherName): Minimum 2, maksimum 50 karakter
  - Doğum Tarihi (birthDate): Geçerli bir tarih formatında olmalıdır
- Müşteri kaydı için aşağıdaki bilgiler opsiyoneldir:
  - Müşteri Sorumlusu ID (accountManagerId): Sistemde kayıtlı ve aktif bir müşteri sorumlusuna ait olmalıdır
- Sistem, her müşteri için otomatik olarak benzersiz bir ID atamalıdır.
- Sistem, kayıt tarihini (createdAt) ve güncelleme tarihini (updatedAt) otomatik olarak atamalıdır.

#### FR-1.1.2 E-posta Benzersizlik Kontrolü
- Sistem, aynı e-posta adresiyle birden fazla müşteri kaydı oluşturulmasını engellemelidir.
- Müşteri güncellemesinde de e-posta benzersizliği kontrol edilmelidir.

#### FR-1.1.3 TC Kimlik No Benzersizlik Kontrolü
- Sistem, aynı TC Kimlik Numarasıyla birden fazla müşteri kaydı oluşturulmasını engellemelidir.
- Müşteri güncellemesinde de TC Kimlik No benzersizliği kontrol edilmelidir.

#### FR-1.1.4 Şifre Güvenliği
- Sistem, müşteri şifrelerini düz metin olarak saklamayıp, bcrypt algoritması ile hashleyerek saklamalıdır.
- Şifre güncellemelerinde de aynı hashleme işlemi uygulanmalıdır.

#### FR-1.1.5 Bireysel Müşteri Listeleme
- Sistem, kayıtlı tüm bireysel müşterileri listeleyebilmelidir.
- Liste, toplam müşteri sayısını (total) içermelidir.
- Her müşteri kaydı, atanmış müşteri sorumlusunun bilgilerini (id ve fullName) içermelidir.

#### FR-1.1.6 Bireysel Müşteri Detay Görüntüleme
- Sistem, belirli bir ID'ye sahip bireysel müşteriyi görüntüleyebilmelidir.
- Müşteri bulunamazsa uygun hata mesajı dönmelidir.
- Müşteri detayında atanmış müşteri sorumlusunun bilgileri görüntülenmelidir.

#### FR-1.1.7 Bireysel Müşteri Güncelleme
- Sistem, mevcut bir bireysel müşterinin bilgilerini güncelleyebilmelidir.
- Güncelleme işleminde sadece gönderilen alanlar güncellenmelidir (kısmi güncelleme).
- Güncelleme tarihini (updatedAt) otomatik olarak yenilemelidir.
- Güncellenebilir alanlar:
  - Ad, Soyad, E-posta, Şifre, TC Kimlik No, Baba Adı, Doğum Tarihi, Müşteri Sorumlusu ID

#### FR-1.1.8 Bireysel Müşteri Silme
- Sistem, belirli bir ID'ye sahip bireysel müşteriyi silebilmelidir.
- Müşteri bulunamazsa uygun hata mesajı dönmelidir.
- Başarılı silme işleminde içerik dönmeden 204 No Content yanıtı verilmelidir.

---

## 2. Müşteri Sorumlusu (Account Manager) Yönetimi

### 2.1 Müşteri Sorumlusu İşlemleri

#### FR-2.1.1 Müşteri Sorumlusu Ekleme
- Sistem, yeni müşteri sorumlusu kaydı oluşturabilmelidir.
- Müşteri sorumlusu kaydı için aşağıdaki bilgiler zorunludur:
  - Ad (firstName): Minimum 2, maksimum 50 karakter
  - Soyad (lastName): Minimum 2, maksimum 50 karakter
  - E-posta (email): Geçerli e-posta formatında olmalıdır
- Müşteri sorumlusu kaydı için aşağıdaki bilgiler opsiyoneldir:
  - Telefon (phone): Maksimum 20 karakter
  - Departman (department): Maksimum 100 karakter
- Sistem, her müşteri sorumlusu için otomatik olarak benzersiz bir ID atamalıdır.
- Yeni oluşturulan müşteri sorumlusu varsayılan olarak aktif (isActive: true) durumda olmalıdır.
- Sistem, kayıt tarihini (createdAt) ve güncelleme tarihini (updatedAt) otomatik olarak atamalıdır.

#### FR-2.1.2 Müşteri Sorumlusu E-posta Benzersizlik Kontrolü
- Sistem, aynı e-posta adresiyle birden fazla müşteri sorumlusu kaydı oluşturulmasını engellemelidir.

#### FR-2.1.3 Müşteri Sorumlusu Listeleme
- Sistem, kayıtlı tüm müşteri sorumlularını listeleyebilmelidir.
- Liste, toplam müşteri sorumlusu sayısını (total) içermelidir.
- Her kayıt, tam ad bilgisini (fullName: ad + soyad) içermelidir.

#### FR-2.1.4 Müşteri Sorumlusu Dropdown Listesi
- Sistem, açılır kutu (dropdown) için sadeleştirilmiş müşteri sorumlusu listesi sağlamalıdır.
- Bu liste sadece aktif müşteri sorumlularını içermelidir.
- Her kayıt sadece id ve fullName alanlarını içermelidir.

#### FR-2.1.5 Müşteri Sorumlusu Detay Görüntüleme
- Sistem, belirli bir ID'ye sahip müşteri sorumlusunu görüntüleyebilmelidir.
- Müşteri sorumlusu bulunamazsa uygun hata mesajı dönmelidir.

#### FR-2.1.6 Müşteri Sorumlusu Güncelleme
- Sistem, mevcut bir müşteri sorumlusunun bilgilerini güncelleyebilmelidir.
- Güncelleme işleminde sadece gönderilen alanlar güncellenmelidir (kısmi güncelleme).
- Güncelleme tarihini (updatedAt) otomatik olarak yenilemelidir.
- Güncellenebilir alanlar:
  - Ad, Soyad, E-posta, Telefon, Departman, Aktiflik Durumu (isActive)

#### FR-2.1.7 Müşteri Sorumlusu Silme
- Sistem, belirli bir ID'ye sahip müşteri sorumlusunu silebilmelidir.
- Müşteri sorumlusu bulunamazsa uygun hata mesajı dönmelidir.
- Başarılı silme işleminde içerik dönmeden 204 No Content yanıtı verilmelidir.

---

## 3. Müşteri - Müşteri Sorumlusu İlişkisi

#### FR-3.1 Müşteri Sorumlusu Atama
- Sistem, bir müşteriye müşteri sorumlusu atanabilmesini sağlamalıdır.
- Atama işlemi müşteri oluşturulurken veya güncellenirken yapılabilmelidir.
- Sadece sistemde kayıtlı ve aktif olan müşteri sorumluları atanabilmelidir.
- Geçersiz veya pasif bir müşteri sorumlusu ID'si ile atama yapılmaya çalışıldığında hata dönmelidir.

#### FR-3.2 Müşteri Sorumlusu Bilgisi Görüntüleme
- Müşteri bilgileri görüntülenirken, atanmış müşteri sorumlusunun id ve fullName bilgileri de görüntülenmelidir.
- Müşteri sorumlusu atanmamışsa bu alan null olarak dönmelidir.

---

## 4. API ve Sistem Gereksinimleri

#### FR-4.1 RESTful API
- Sistem, RESTful mimari prensiplerine uygun API sağlamalıdır.
- API versiyonlama desteklenmelidir (v1).

#### FR-4.2 API Dokümantasyonu
- Sistem, otomatik API dokümantasyonu sağlamalıdır.
- Swagger UI (/docs) üzerinden interaktif dokümantasyon erişilebilir olmalıdır.
- ReDoc (/redoc) üzerinden alternatif dokümantasyon erişilebilir olmalıdır.
- OpenAPI JSON spesifikasyonu (/openapi.json) erişilebilir olmalıdır.

#### FR-4.3 Sağlık Kontrolü
- Sistem, sağlık kontrolü için endpoint sağlamalıdır (/health).
- Bu endpoint sistemin çalışır durumda olup olmadığını kontrol etmeye yarar.

#### FR-4.4 CORS Desteği
- Sistem, Cross-Origin Resource Sharing (CORS) desteği sağlamalıdır.
- İzin verilen origin'ler, metodlar ve header'lar yapılandırılabilir olmalıdır.

#### FR-4.5 Validasyon
- Sistem, gelen isteklerdeki verileri otomatik olarak doğrulamalıdır.
- Geçersiz veri durumunda anlamlı hata mesajları dönmelidir.
- HTTP 400 Bad Request kodu ile validasyon hataları bildirilmelidir.
- HTTP 404 Not Found kodu ile bulunamayan kaynaklar bildirilmelidir.

---

## 5. Müşteri Tipleri

#### FR-5.1 Bireysel Müşteri
- Sistem, bireysel (gerçek kişi) müşteri tipini desteklemelidir.
- Bireysel müşteriler için TC Kimlik No zorunludur.

#### FR-5.2 Kurumsal Müşteri (Gelecek Geliştirme)
- Sistem, kurumsal müşteri tipi için genişletilebilir yapıda olmalıdır.
- Bu özellik gelecek sürümlerde eklenecektir.

---

## API Endpoint Özeti

| Modül | Metod | Endpoint | Açıklama |
|-------|-------|----------|----------|
| Müşteri | POST | /api/v1/customers/individual/ | Yeni bireysel müşteri oluştur |
| Müşteri | GET | /api/v1/customers/individual/ | Tüm bireysel müşterileri listele |
| Müşteri | GET | /api/v1/customers/individual/{id} | ID'ye göre müşteri getir |
| Müşteri | PUT | /api/v1/customers/individual/{id} | Müşteri bilgilerini güncelle |
| Müşteri | DELETE | /api/v1/customers/individual/{id} | Müşteri sil |
| Account Manager | POST | /api/v1/account-managers/ | Yeni müşteri sorumlusu oluştur |
| Account Manager | GET | /api/v1/account-managers/ | Tüm müşteri sorumlularını listele |
| Account Manager | GET | /api/v1/account-managers/dropdown | Dropdown için liste |
| Account Manager | GET | /api/v1/account-managers/{id} | ID'ye göre müşteri sorumlusu getir |
| Account Manager | PUT | /api/v1/account-managers/{id} | Müşteri sorumlusu güncelle |
| Account Manager | DELETE | /api/v1/account-managers/{id} | Müşteri sorumlusu sil |
| Sistem | GET | / | API bilgisi |
| Sistem | GET | /health | Sağlık kontrolü |
| Auth | POST | /api/v1/auth/login | Kullanıcı girişi |
| Auth | GET | /api/v1/auth/me | Mevcut kullanıcı bilgisi |
| Auth | POST | /api/v1/auth/validate | Token doğrulama |
| Auth | GET | /api/v1/auth/users | Tüm kullanıcılar (Admin) |
| Auth | GET | /api/v1/auth/users/type/{type} | Tipe göre kullanıcılar (Admin) |

---

## 6. Kimlik Doğrulama (Authentication)

### 6.1 Kullanıcı Tipleri

#### FR-6.1.1 Kullanıcı Tipi Tanımları
- Sistem, iki farklı kullanıcı tipini desteklemelidir:
  - **admin**: Sistem yöneticisi - tüm yetkilere sahip
  - **cc**: Customer Care / Müşteri Temsilcisi - sınırlı yetkiler

### 6.2 Kullanıcı Girişi (Login)

#### FR-6.2.1 Başarılı Giriş
- Sistem, geçerli kullanıcı adı ve şifre ile giriş yapılabilmesini sağlamalıdır.
- Başarılı giriş sonrası JWT access token dönmelidir.
- Token yanıtı aşağıdaki bilgileri içermelidir:
  - access_token: JWT token string
  - token_type: "bearer"
  - expires_in: Token süresi (saniye)
  - user: Kullanıcı bilgileri (id, username, email, fullName, userType)

#### FR-6.2.2 Geçersiz Kimlik Bilgileri
- Yanlış kullanıcı adı veya şifre ile giriş denemesinde HTTP 401 Unauthorized dönmelidir.
- Hata mesajı: "Incorrect username or password"

#### FR-6.2.3 Kullanıcı Durumu Kontrolü
- Pasif (isActive: false) kullanıcılar sisteme giriş yapamamalıdır.

### 6.3 Token Yönetimi

#### FR-6.3.1 JWT Token Yapısı
- Token, HS256 algoritması ile imzalanmalıdır.
- Token payload içeriği:
  - user_id: Kullanıcı ID
  - username: Kullanıcı adı
  - user_type: Kullanıcı tipi (admin/cc)
  - exp: Token son geçerlilik zamanı

#### FR-6.3.2 Token Süresi
- Access token varsayılan olarak 30 dakika geçerli olmalıdır.
- Token süresi yapılandırılabilir olmalıdır.

#### FR-6.3.3 Token Doğrulama
- Sistem, gelen token'ın geçerliliğini kontrol edebilmelidir.
- Geçersiz veya süresi dolmuş token için HTTP 401 dönmelidir.
- Geçerli token için kullanıcı bilgilerini dönmelidir.

### 6.4 Korumalı Endpoint'ler

#### FR-6.4.1 Token Zorunluluğu
- Korumalı endpoint'lere erişim için geçerli Bearer token gereklidir.
- Token, Authorization header'ında "Bearer <token>" formatında gönderilmelidir.
- Token eksikse HTTP 403 Forbidden dönmelidir.
- Token geçersizse HTTP 401 Unauthorized dönmelidir.

#### FR-6.4.2 Yetkilendirme (Authorization)
- Bazı endpoint'ler sadece admin kullanıcılar tarafından erişilebilir olmalıdır.
- cc kullanıcılar admin-only endpoint'lere erişmeye çalıştığında HTTP 403 dönmelidir.
- Hata mesajı: "Admin privileges required"

### 6.5 Kullanıcı Bilgisi Endpoint'leri

#### FR-6.5.1 Mevcut Kullanıcı Bilgisi (/me)
- Giriş yapmış kullanıcı kendi bilgilerini görüntüleyebilmelidir.
- Yanıt: id, username, email, fullName, userType

#### FR-6.5.2 Tüm Kullanıcıları Listeleme
- Sadece admin kullanıcılar tüm kullanıcıları listeleyebilmelidir.
- Yanıt: Kullanıcı listesi (şifre hariç)

#### FR-6.5.3 Tipe Göre Kullanıcı Listeleme
- Sadece admin kullanıcılar belirli tipteki kullanıcıları listeleyebilmelidir.
- Geçerli tipler: admin, cc

---

## 7. Test Senaryoları (API Test Cases)

### 7.1 Müşteri Yönetimi Test Senaryoları

#### TC-API-1.1: Müşteri Oluşturma - Başarılı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-1.1 |
| **Endpoint** | POST /api/v1/customers/individual/ |
| **Önkoşul** | - |
| **Test Verisi** | `{"firstName": "Ali", "lastName": "Veli", "email": "ali@test.com", "password": "Test123!", "natId": "12345678901", "fatherName": "Ahmet", "birthDate": "1990-01-15"}` |
| **Beklenen Sonuç** | HTTP 201, Müşteri bilgileri döner, password response'da yok |

#### TC-API-1.2: Müşteri Oluşturma - Eksik Zorunlu Alan
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-1.2 |
| **Endpoint** | POST /api/v1/customers/individual/ |
| **Önkoşul** | - |
| **Test Verisi** | `{"firstName": "Ali"}` |
| **Beklenen Sonuç** | HTTP 422, Validation error detayları |

#### TC-API-1.3: Müşteri Oluşturma - Tekrarlayan E-posta
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-1.3 |
| **Endpoint** | POST /api/v1/customers/individual/ |
| **Önkoşul** | ali@test.com e-postası ile müşteri mevcut |
| **Test Verisi** | `{"firstName": "Mehmet", "lastName": "Demir", "email": "ali@test.com", "password": "Test123!", "natId": "98765432109", "fatherName": "Kemal", "birthDate": "1985-05-20"}` |
| **Beklenen Sonuç** | HTTP 400, "Email already exists" |

#### TC-API-1.4: Müşteri Oluşturma - Tekrarlayan TC Kimlik No
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-1.4 |
| **Endpoint** | POST /api/v1/customers/individual/ |
| **Önkoşul** | 12345678901 natId ile müşteri mevcut |
| **Test Verisi** | `{"firstName": "Mehmet", "lastName": "Demir", "email": "mehmet@test.com", "password": "Test123!", "natId": "12345678901", "fatherName": "Kemal", "birthDate": "1985-05-20"}` |
| **Beklenen Sonuç** | HTTP 400, "National ID already exists" |

#### TC-API-1.5: Müşteri Listeleme - Başarılı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-1.5 |
| **Endpoint** | GET /api/v1/customers/individual/ |
| **Önkoşul** | En az 1 müşteri kayıtlı |
| **Beklenen Sonuç** | HTTP 200, `{"items": [...], "total": n}` |

#### TC-API-1.6: Müşteri Listeleme - Boş Liste
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-1.6 |
| **Endpoint** | GET /api/v1/customers/individual/ |
| **Önkoşul** | Hiç müşteri yok |
| **Beklenen Sonuç** | HTTP 200, `{"items": [], "total": 0}` |

#### TC-API-1.7: Müşteri Detay - Başarılı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-1.7 |
| **Endpoint** | GET /api/v1/customers/individual/{id} |
| **Önkoşul** | ID=1 olan müşteri mevcut |
| **Beklenen Sonuç** | HTTP 200, Müşteri detayları |

#### TC-API-1.8: Müşteri Detay - Bulunamadı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-1.8 |
| **Endpoint** | GET /api/v1/customers/individual/9999 |
| **Önkoşul** | ID=9999 olan müşteri yok |
| **Beklenen Sonuç** | HTTP 404, "Customer not found" |

#### TC-API-1.9: Müşteri Güncelleme - Başarılı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-1.9 |
| **Endpoint** | PUT /api/v1/customers/individual/{id} |
| **Önkoşul** | ID=1 olan müşteri mevcut |
| **Test Verisi** | `{"firstName": "Ali Updated"}` |
| **Beklenen Sonuç** | HTTP 200, Güncellenmiş bilgiler, updatedAt değişmiş |

#### TC-API-1.10: Müşteri Güncelleme - Bulunamadı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-1.10 |
| **Endpoint** | PUT /api/v1/customers/individual/9999 |
| **Test Verisi** | `{"firstName": "Test"}` |
| **Beklenen Sonuç** | HTTP 404 |

#### TC-API-1.11: Müşteri Silme - Başarılı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-1.11 |
| **Endpoint** | DELETE /api/v1/customers/individual/{id} |
| **Önkoşul** | ID=1 olan müşteri mevcut |
| **Beklenen Sonuç** | HTTP 204, No Content |

#### TC-API-1.12: Müşteri Silme - Bulunamadı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-1.12 |
| **Endpoint** | DELETE /api/v1/customers/individual/9999 |
| **Beklenen Sonuç** | HTTP 404 |

### 7.2 Müşteri Sorumlusu Test Senaryoları

#### TC-API-2.1: Müşteri Sorumlusu Oluşturma - Başarılı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-2.1 |
| **Endpoint** | POST /api/v1/account-managers/ |
| **Test Verisi** | `{"firstName": "Manager", "lastName": "Test", "email": "manager@test.com"}` |
| **Beklenen Sonuç** | HTTP 201, isActive: true, fullName: "Manager Test" |

#### TC-API-2.2: Müşteri Sorumlusu Dropdown - Sadece Aktif
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-2.2 |
| **Endpoint** | GET /api/v1/account-managers/dropdown |
| **Önkoşul** | 1 aktif, 1 pasif manager mevcut |
| **Beklenen Sonuç** | HTTP 200, Sadece aktif manager listede, format: `[{"id": n, "fullName": "..."}]` |

### 7.3 Müşteri - Sorumlu İlişki Test Senaryoları

#### TC-API-3.1: Müşteri Oluşturma - Sorumlu Atama
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-3.1 |
| **Endpoint** | POST /api/v1/customers/individual/ |
| **Önkoşul** | ID=1 olan aktif manager mevcut |
| **Test Verisi** | `{"firstName": "Ali", "lastName": "Veli", "email": "ali@test.com", "password": "Test123!", "natId": "12345678901", "fatherName": "Ahmet", "birthDate": "1990-01-15", "accountManagerId": 1}` |
| **Beklenen Sonuç** | HTTP 201, accountManager: {"id": 1, "fullName": "..."} |

#### TC-API-3.2: Müşteri Oluşturma - Geçersiz Sorumlu ID
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-3.2 |
| **Endpoint** | POST /api/v1/customers/individual/ |
| **Test Verisi** | `{..., "accountManagerId": 9999}` |
| **Beklenen Sonuç** | HTTP 400, "Account Manager not found" |

#### TC-API-3.3: Müşteri Oluşturma - Pasif Sorumlu
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-3.3 |
| **Endpoint** | POST /api/v1/customers/individual/ |
| **Önkoşul** | ID=2 olan pasif manager mevcut |
| **Test Verisi** | `{..., "accountManagerId": 2}` |
| **Beklenen Sonuç** | HTTP 400, "Account Manager is not active" |

### 7.4 Authentication Test Senaryoları

#### TC-API-4.1: Login - Admin Başarılı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-4.1 |
| **Endpoint** | POST /api/v1/auth/login |
| **Test Verisi** | `{"username": "admin", "password": "admin123"}` |
| **Beklenen Sonuç** | HTTP 200, access_token mevcut, user.userType: "admin" |

#### TC-API-4.2: Login - CC Başarılı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-4.2 |
| **Endpoint** | POST /api/v1/auth/login |
| **Test Verisi** | `{"username": "cc1", "password": "cc123"}` |
| **Beklenen Sonuç** | HTTP 200, access_token mevcut, user.userType: "cc" |

#### TC-API-4.3: Login - Geçersiz Kullanıcı Adı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-4.3 |
| **Endpoint** | POST /api/v1/auth/login |
| **Test Verisi** | `{"username": "invalid", "password": "password"}` |
| **Beklenen Sonuç** | HTTP 401, "Incorrect username or password" |

#### TC-API-4.4: Login - Geçersiz Şifre
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-4.4 |
| **Endpoint** | POST /api/v1/auth/login |
| **Test Verisi** | `{"username": "admin", "password": "wrongpass"}` |
| **Beklenen Sonuç** | HTTP 401, "Incorrect username or password" |

#### TC-API-4.5: Me Endpoint - Geçerli Token
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-4.5 |
| **Endpoint** | GET /api/v1/auth/me |
| **Önkoşul** | Admin olarak login yapılmış |
| **Header** | Authorization: Bearer {token} |
| **Beklenen Sonuç** | HTTP 200, username: "admin" |

#### TC-API-4.6: Me Endpoint - Token Yok
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-4.6 |
| **Endpoint** | GET /api/v1/auth/me |
| **Header** | - |
| **Beklenen Sonuç** | HTTP 403 |

#### TC-API-4.7: Me Endpoint - Geçersiz Token
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-4.7 |
| **Endpoint** | GET /api/v1/auth/me |
| **Header** | Authorization: Bearer invalid_token |
| **Beklenen Sonuç** | HTTP 401, "Could not validate credentials" |

#### TC-API-4.8: Token Doğrulama - Başarılı
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-4.8 |
| **Endpoint** | POST /api/v1/auth/validate |
| **Önkoşul** | Geçerli token mevcut |
| **Header** | Authorization: Bearer {token} |
| **Beklenen Sonuç** | HTTP 200, Kullanıcı bilgileri |

#### TC-API-4.9: Users Endpoint - Admin Erişimi
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-4.9 |
| **Endpoint** | GET /api/v1/auth/users |
| **Önkoşul** | Admin olarak login |
| **Header** | Authorization: Bearer {admin_token} |
| **Beklenen Sonuç** | HTTP 200, 5 kullanıcı listesi |

#### TC-API-4.10: Users Endpoint - CC Erişim Engeli
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-4.10 |
| **Endpoint** | GET /api/v1/auth/users |
| **Önkoşul** | CC olarak login |
| **Header** | Authorization: Bearer {cc_token} |
| **Beklenen Sonuç** | HTTP 403, "Admin privileges required" |

#### TC-API-4.11: Users By Type - Admin Tipi
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-4.11 |
| **Endpoint** | GET /api/v1/auth/users/type/admin |
| **Önkoşul** | Admin olarak login |
| **Header** | Authorization: Bearer {admin_token} |
| **Beklenen Sonuç** | HTTP 200, 2 admin kullanıcı |

#### TC-API-4.12: Users By Type - CC Tipi
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-4.12 |
| **Endpoint** | GET /api/v1/auth/users/type/cc |
| **Önkoşul** | Admin olarak login |
| **Header** | Authorization: Bearer {admin_token} |
| **Beklenen Sonuç** | HTTP 200, 3 cc kullanıcı |

### 7.5 Sistem Test Senaryoları

#### TC-API-5.1: Health Check
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-5.1 |
| **Endpoint** | GET /health |
| **Beklenen Sonuç** | HTTP 200, `{"status": "healthy"}` |

#### TC-API-5.2: Root Endpoint
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-5.2 |
| **Endpoint** | GET / |
| **Beklenen Sonuç** | HTTP 200, message, version, status içerir |

#### TC-API-5.3: Swagger UI Erişimi
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-5.3 |
| **Endpoint** | GET /docs |
| **Beklenen Sonuç** | HTTP 200, HTML içerik |

#### TC-API-5.4: OpenAPI JSON Erişimi
| Alan | Değer |
|------|-------|
| **Test ID** | TC-API-5.4 |
| **Endpoint** | GET /openapi.json |
| **Beklenen Sonuç** | HTTP 200, openapi, info, paths içerir |

---

## Fake Kullanıcı Bilgileri

| Username | Password | User Type | Full Name |
|----------|----------|-----------|-----------|
| admin | admin123 | admin | System Admin |
| manager | manager123 | admin | John Manager |
| cc1 | cc123 | cc | Ahmet Yılmaz |
| cc2 | cc123 | cc | Mehmet Demir |
| cc3 | cc123 | cc | Ayşe Kaya |
