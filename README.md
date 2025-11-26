# CRM Backend Application

FastAPI tabanlı profesyonel CRM uygulaması.

## Gereksinimler

- Python 3.11
- PostgreSQL
- Redis (opsiyonel, caching için)

## Kurulum

1. Virtual environment oluşturun:
```cmd
python -m venv venv
venv\Scripts\activate
```

2. Bağımlılıkları yükleyin:
```cmd
pip install -r requirements.txt
```

3. Environment dosyasını oluşturun:
```cmd
copy .env.example .env
```

4. `.env` dosyasını kendi ayarlarınıza göre düzenleyin.

5. Veritabanı migration'larını çalıştırın:
```cmd
alembic upgrade head
```

6. Uygulamayı başlatın:
```cmd
python main.py
```

veya

```cmd
uvicorn main:app --reload
```

## Proje Yapısı

```
crm_backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/      # API endpoint'leri
│   ├── core/                   # Temel konfigürasyon
│   ├── db/                     # Veritabanı bağlantısı
│   ├── models/                 # SQLAlchemy modelleri
│   ├── schemas/                # Pydantic şemaları
│   ├── services/               # İş mantığı
│   ├── utils/                  # Yardımcı fonksiyonlar
│   └── middleware/             # Middleware'ler
├── tests/                      # Test dosyaları
├── alembic/                    # Database migration'lar
├── main.py                     # Ana uygulama
├── requirements.txt            # Python bağımlılıkları
├── .env.example                # Örnek environment dosyası
└── .gitignore                  # Git ignore dosyası
```

## API Dokümantasyonu

Uygulama çalıştırıldıktan sonra:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Lisans

MIT
