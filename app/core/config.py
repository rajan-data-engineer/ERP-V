#DB ENGINE + CONFIGURATION + SECURITY (FOUNDATION)
import os
from functools import lru_cache

class Settings:
    PROJECT_NAME: str = "ERP-V"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    GMAIL_USER: str = os.getenv("GMAIL_USER", "")
    GMAIL_APP_PASSWORD: str = os.getenv("GMAIL_APP_PASSWORD", "")
    AI_ENABLED: bool = False  # AI DISABLED MODE

@lru_cache()
def get_settings():
    return Settings()
