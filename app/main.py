from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.core.config import get_settings
from app.db.session import engine

# Routers
from app.routers.auth_routes import router as auth_router
from app.routers.admin_routes import router as admin_router
from app.routers.account_routes import router as account_router
from app.routers.journal_routes import router as journal_router
from app.routers.ledger_routes import router as ledger_router
from app.routers.products import router as products_router
from app.routers.inventory import router as inventory_router
from app.routers.customers import router as customers_router
from app.routers.sales_orders import router as sales_router
from app.routers.dashboard import router as dashboard_router

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

    # ---------------------------------------
    # CORS CONFIG
    # ---------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # You can restrict later for security
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---------------------------------------
    # ROUTERS
    # ---------------------------------------
    app.include_router(auth_router)
    app.include_router(admin_router)
    app.include_router(account_router)
    app.include_router(journal_router)
    app.include_router(ledger_router)
    app.include_router(products_router)
    app.include_router(inventory_router)
    app.include_router(customers_router)
    app.include_router(sales_router)
    app.include_router(dashboard_router)

    # ---------------------------------------
    # STARTUP EVENT: AUTO-CREATE TABLES
    # ---------------------------------------
    @app.on_event("startup")
    def on_startup():
        print("Initializing ERP-V database...")
        SQLModel.metadata.create_all(engine)
        print("Database initialized successfully.")

    # ---------------------------------------
    # ROOT ENDPOINT
    # ---------------------------------------
    @app.get("/")
    def root():
        return {
            "status": "ok",
            "message": f"{settings.PROJECT_NAME} Backend Running",
            "version": settings.VERSION
        }

    return app


app = create_app()
