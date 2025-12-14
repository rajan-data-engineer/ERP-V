# app/core/config.py

import os
from functools import lru_cache


class Settings:
    PROJECT_NAME: str = "ERP-V"

    # -------------------------
    # DATABASE
    # -------------------------
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # -------------------------
    # SECURITY
    # -------------------------
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-prod")

    # -------------------------
    # EMAIL (REAL SMTP)
    # -------------------------
    GMAIL_USER: str = os.getenv("GMAIL_USER", "")
    GMAIL_APP_PASSWORD: str = os.getenv("GMAIL_APP_PASSWORD", "")

    # -------------------------
    # AI (DISABLED FOR NOW)
    # -------------------------
    AI_ENABLED: bool = False

    # -------------------------
    # SYSTEM META
    # -------------------------
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")


@lru_cache()
def get_settings():
    return Settings()
