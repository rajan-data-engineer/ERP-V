from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.user import User
from app.models.journal import JournalEntry
from app.models.ledger import Ledger
from app.models.audit_log import AuditLog
from app.dependencies.auth_dependency import require_role
from app.services.export_service import ExportService

router = APIRouter(prefix="/admin", tags=["Admin"])


# -------------------------------------------
# LIST ALL USERS
# -------------------------------------------
@router.get("/users")
def list_users(
    session: Session = Depends(get_session),
    admin=Depends(require_role("admin"))
):
    return session.exec(select(User)).all()


# -------------------------------------------
# APPROVE NEW USER
# -------------------------------------------
@router.post("/approve/{user_id}")
def approve_user(
    user_id: int,
    session: Session = Depends(get_session),
    admin=Depends(require_role("admin"))
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found.")

    user.is_active = True
    session.add(user)
    session.commit()

    return {"message": f"User '{user.username}' approved successfully."}


# -------------------------------------------
# UPDATE USER ROLE
# -------------------------------------------
@router.post("/role/{user_id}")
def update_role(
    user_id: int,
    new_role: str,
    session: Session = Depends(get_session),
    admin=Depends(require_role("admin"))
):
    if new_role not in ["viewer", "accountant", "admin"]:
        raise HTTPException(400, "Invalid role. Allowed: viewer, accountant, admin.")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found.")

    user.role = new_role
    session.add(user)
    session.commit()

    return {"message": f"Updated role to '{new_role}' for user '{user.username}'."}


# -------------------------------------------
# EXPORT TABLES TO EXCEL
# -------------------------------------------
@router.get("/export/{table_name}")
def export_table(
    table_name: str,
    session: Session = Depends(get_session),
    admin=Depends(require_role("admin"))
):

    model_map = {
        "users": User,
        "journals": JournalEntry,
        "ledger": Ledger,
        "audit": AuditLog
    }

    if table_name not in model_map:
        raise HTTPException(400, "Invalid table. Allowed: users, journals, ledger, audit.")

    model = model_map[table_name]

    return ExportService.export_table(session, model)


# -------------------------------------------
# AUDIT LOG VIEWER
# -------------------------------------------
@router.get("/audit")
def view_audit_logs(
    session: Session = Depends(get_session),
    admin=Depends(require_role("admin"))
):
    logs = session.exec(
        select(AuditLog).order_by(AuditLog.timestamp.desc())
    ).all()
    return logs
