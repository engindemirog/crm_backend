from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import customers, account_managers, auth

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## CRM (Customer Relationship Management) API
    
    Bu API, müşteri ilişkileri yönetimi için geliştirilmiş profesyonel bir backend uygulamasıdır.
    
    ### Özellikler:
    
    * **Bireysel Müşteri Yönetimi**: Bireysel müşterileri ekleyin, listeleyin, güncelleyin ve silin
    * **Müşteri Sorumlusu Yönetimi**: Account Manager'ları yönetin ve müşterilere atayın
    * **Güvenlik**: Şifre hashleme ve güvenli veri saklama
    * **Validasyon**: Email, TC Kimlik No ve diğer alanlar için otomatik doğrulama
    
    ### Müşteri Tipleri:
    
    * **Bireysel Müşteriler**: Gerçek kişi müşteriler
    * **Kurumsal Müşteriler**: (Yakında eklenecek)
    """,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "CRM Support Team",
        "email": "support@crm.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    terms_of_service="https://crm.com/terms/",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Include routers
app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(account_managers.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to CRM API",
        "version": settings.APP_VERSION,
        "status": "active"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
