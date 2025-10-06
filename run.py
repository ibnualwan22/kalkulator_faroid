"""
Entry point untuk menjalankan aplikasi Kalkulator Faroid
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("="*60)
    print("🕌 KALKULATOR FAROID - API Server")
    print("="*60)
    print(f"App Name    : {settings.APP_NAME}")
    print(f"Version     : {settings.APP_VERSION}")
    print(f"Environment : {settings.ENVIRONMENT}")
    print(f"Debug Mode  : {settings.DEBUG}")
    print(f"Host        : {settings.HOST}:{settings.PORT}")
    print(f"Database    : {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Not configured'}")
    print("="*60)
    print(f"\n📖 API Documentation:")
    print(f"   Swagger UI : http://{settings.HOST}:{settings.PORT}/docs")
    print(f"   ReDoc      : http://{settings.HOST}:{settings.PORT}/redoc")
    print("\n🚀 Starting server...\n")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
