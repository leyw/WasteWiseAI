import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import get_settings
from core.database import create_tables
from routers import health, auth, analyze, history, statistics, guides

# Reset lru_cache agar .env dibaca ulang setiap kali uvicorn --reload
get_settings.cache_clear()
settings = get_settings()

# ── Inisialisasi aplikasi ──────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description="API untuk klasifikasi sampah berbasis AI.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files (gambar yang diupload) ───────────────────────────────────────
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(analyze.router)
app.include_router(history.router)
app.include_router(statistics.router)
app.include_router(guides.router)


# ── Startup ───────────────────────────────────────────────────────────────────
@app.on_event("startup")
def on_startup():
    """Jalankan saat aplikasi pertama kali distart."""
    from core.database import SessionLocal
    from services.seed_guides import seed_guides

    create_tables()

    db = SessionLocal()
    try:
        seed_guides(db)
    finally:
        db.close()

    print(f"[OK] {settings.APP_NAME} backend berjalan.")
    print(f"     AI Provider : {settings.AI_PROVIDER}")
    print(f"     AI Model    : {settings.GEMINI_MODEL}")
    print(f"     Database    : {settings.DATABASE_URL}")
    print(f"     Upload Dir  : {settings.UPLOAD_DIR}")
