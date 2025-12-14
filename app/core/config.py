# app/core/config.py
import os
from functools import lru_cache


class Settings:
    PROJECT_NAME: str = "ERP-V"

    # ------------------------------
    # DATABASE CONFIG
    # ------------------------------
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # ------------------------------
    # SECURITY / TOKENS
    # ------------------------------
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")

    # ------------------------------
    # EMAIL NOTIFICATIONS (OPTIONAL)
    # ------------------------------
    GMAIL_USER: str = os.getenv("GMAIL_USER", "")
    GMAIL_APP_PASSWORD: str = os.getenv("GMAIL_APP_PASSWORD", "")

    # ------------------------------
    # AI MODE (DISABLED FOR FREE TIER)
    # ------------------------------
    AI_ENABLED: bool = False  # Keep disabled to avoid OpenAI billing

    # ------------------------------
    # SYSTEM META
    # ------------------------------
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")  # for Render


@lru_cache()
def get_settings() -> Settings:
    return Settings()
