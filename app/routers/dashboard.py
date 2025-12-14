# app/routers/dashboard.py

from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
def dashboard_root():
    return {"message": "Dashboard stats coming soon"}
