# app/routers/admin_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.user import User
from app.dependencies.auth_dependency import require_role
from app.services.email_service_wrapper import EmailNotifications
from app.services.excel_export import ExcelExportService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users")
def list_users(
    session: Session = Depends(get_session),
    admin=Depends(require_role("admin"))
):
    return session.exec(select(User)).all()


@router.post("/approve/{user_id}")
def approve_user(
    user_id: int,
    session: Session = Depends(get_session),
    admin=Depends(require_role("admin"))
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.is_active = True
    session.commit()

    if user.email:
        EmailNotifications.notify_user_approved(user.email)

    return {"message": f"User '{user.username}' approved"}


@router.post("/role/{user_id}")
def update_role(
    user_id: int,
    role: str,
    session: Session = Depends(get_session),
    admin=Depends(require_role("admin"))
):
    if role not in ["viewer", "accountant", "admin"]:
        raise HTTPException(400, "Invalid role")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.role = role
    session.commit()

    return {"message": f"Role updated for {user.username}"}
