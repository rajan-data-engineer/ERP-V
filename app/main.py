from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import SQLModel
from app.db.session import engine
from app.core.audit import AuditMiddleware

# Routers
from app.routers.auth_routes import router as auth_router
from app.routers.admin_routes import router as admin_router
from app.routers.journal_routes import router as journal_router
from app.routers.ledger_routes import router as ledger_router
from app.routers.products import router as products_router
from app.routers.customers import router as customers_router
from app.routers.inventory import router as inventory_router
from app.routers.sales_orders import router as sales_orders_router


app = FastAPI(title="ERP-V Backend", version="1.0")


# ---------------------------------------------------------
# CORS SETTINGS (Frontend compatibility)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# GLOBAL AUDIT LOGGING MIDDLEWARE
# ---------------------------------------------------------
app.add_middleware(AuditMiddleware)


# ---------------------------------------------------------
# DATABASE INITIALIZATION ON STARTUP
# ---------------------------------------------------------
@app.on_event("startup")
def startup_event():
    SQLModel.metadata.create_all(engine)


# ---------------------------------------------------------
# ROUTER REGISTRATION
# ---------------------------------------------------------
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(journal_router)
app.include_router(ledger_router)
app.include_router(products_router)
app.include_router(customers_router)
app.include_router(inventory_router)
app.include_router(sales_orders_router)


# ---------------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"message": "ERP-V backend running successfully"}


