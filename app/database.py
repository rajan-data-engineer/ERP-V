import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# Load environment variables (.env for local, Render uses internal env vars)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing. Set it in Render environment variables.")

# Create SQLModel engine
engine = create_engine(DATABASE_URL, echo=False)


# Provide session to routers
def get_session():
    with Session(engine) as session:
        yield session


# Create tables on startup
def init_db():
    SQLModel.metadata.create_all(engine)
