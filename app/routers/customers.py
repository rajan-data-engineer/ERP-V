# app/routers/customers.py

from fastapi import APIRouter

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/")
def customers_root():
    return {"message": "Customers endpoint placeholder"}
