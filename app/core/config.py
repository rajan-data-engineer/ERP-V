import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "ERP-V Backend"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    GMAIL_USER: str = os.getenv("GMAIL_USER")
    GMAIL_APP_PASSWORD: str = os.getenv("GMAIL_APP_PASSWORD")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    PYTHON_VERSION: str = os.getenv("PYTHON_VERSION", "3.10")

settings = Settings()
