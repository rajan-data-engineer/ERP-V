# app/routers/inventory.py

from fastapi import APIRouter

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/")
def inventory_root():
    return {"message": "Inventory endpoint placeholder"}
