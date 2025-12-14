from sqlmodel import create_engine, Session
from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, echo=False)


def get_session():
    with Session(engine) as session:
        yield session
