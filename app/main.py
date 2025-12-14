from fastapi import FastAPI
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_routes, admin_routes
from app.db.session import engine
from sqlmodel import SQLModel
from app.models import accounting
from app.routers import journal, ledger
from app.database import init_db

app = FastAPI(title="ERP-V Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
app.include_router(journal.router)
app.include_router(ledger.router)

@app.get("/")
def root():
    return {"status": "ERP-V Backend Running"}
