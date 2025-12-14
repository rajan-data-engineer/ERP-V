# app/routers/products.py

from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def list_products():
    return {"message": "Products endpoint placeholder"}
