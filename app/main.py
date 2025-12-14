from fastapi import FastAPI
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_routes, admin_routes
from app.db.session import engine
from sqlmodel import SQLModel

app = FastAPI(title="ERP-V Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(auth_routes.router)
app.include_router(admin_routes.router)


@app.get("/")
def root():
    return {"status": "ERP-V Backend Running"}
