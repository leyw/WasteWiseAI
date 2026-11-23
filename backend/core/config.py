from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "WasteWise AI"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str = "changeme-generate-a-strong-random-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 jam

    # Database
    DATABASE_URL: str = "sqlite:///./wastewise.db"

    # AI Provider
    AI_PROVIDER: str = "mock"  # "mock" | "gemini" | "openai"
    AI_API_KEY: str = ""
    GEMINI_MODEL: str = "models/gemini-3-flash-preview"  # model Gemini yang mendukung vision

    # Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 5
    ALLOWED_EXTENSIONS: list = ["jpg", "jpeg", "png", "webp"]

    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://127.0.0.1:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
