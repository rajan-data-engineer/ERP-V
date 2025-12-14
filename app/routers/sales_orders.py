# app/routers/sales_orders.py

from fastapi import APIRouter

router = APIRouter(prefix="/sales", tags=["Sales Orders"])

@router.get("/")
def sales_root():
    return {"message": "Sales orders endpoint placeholder"}
