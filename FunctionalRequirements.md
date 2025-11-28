# CRM Application - Fonksiyonel Gereksinimler

## Doküman Bilgileri
- **Proje Adı:** CRM (Customer Relationship Management) Application
- **Versiyon:** 1.0.0
- **Tarih:** 28 Kasım 2025

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
