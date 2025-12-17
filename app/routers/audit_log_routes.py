from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies.auth_dependency import require_role
from app.services.audit_log_service import AuditLogService

router = APIRouter(prefix="/audit", tags=["Audit Logs"])


# ----------------------------------------------
# LIST AUDIT LOGS
# ----------------------------------------------
@router.get("/")
def list_audit_logs(
    user_id: int = None,
    action: str = None,
    date_from: str = None,
    date_to: str = None,
    search: str = None,
    limit: int = 200,
    offset: int = 0,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    return AuditLogService.list_logs(
        session=session,
        user_id=user_id,
        action=action,
        date_from=date_from,
        date_to=date_to,
        search=search,
        limit=limit,
        offset=offset
    )


# ----------------------------------------------
# LIST DISTINCT ACTION TYPES
# ----------------------------------------------
@router.get("/actions")
def audit_actions(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    return AuditLogService.list_actions(session)
