from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func

from app.db.session import get_session
from app.models.user import User
from app.models.journal import JournalEntry
from app.models.ledger import LedgerEntry
from app.models.fiscal import FiscalPeriod
from app.models.audit_log import AuditLog
from app.dependencies.auth_dependency import require_role
from datetime import datetime, timedelta

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/overview")
def get_dashboard_overview(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin"))
):
    # ------------------------------
    # User Counts
    # ------------------------------
    total_users = session.exec(select(func.count()).select_from(User)).one()
    active_users = session.exec(
        select(func.count()).where(User.is_active == True)
    ).one()
    inactive_users = total_users - active_users

    # ------------------------------
    # Journals
    # ------------------------------
    total_journals = session.exec(
        select(func.count()).select_from(JournalEntry)
    ).one()

    posted_journals = session.exec(
        select(func.count()).where(JournalEntry.status == "posted")
    ).one()

    draft_journals = total_journals - posted_journals

    # ------------------------------
    # Ledger Entries
    # ------------------------------
    ledger_count = session.exec(
        select(func.count()).select_from(LedgerEntry)
    ).one()

    # ------------------------------
    # Fiscal Periods
    # ------------------------------
    fiscal_periods = session.exec(
        select(func.count()).select_from(FiscalPeriod)
    ).one()

    # ------------------------------
    # Recent Audit Events
    # ------------------------------
    recent_audit = session.exec(
        select(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .limit(10)
    ).all()

    # ------------------------------
    # Activity in Last 7 Days
    # ------------------------------
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    activity_last_7_days = session.exec(
        select(func.count()).where(AuditLog.timestamp >= seven_days_ago)
    ).one()

    # ------------------------------
    # Response
    # ------------------------------
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "inactive": inactive_users,
        },
        "journals": {
            "total": total_journals,
            "posted": posted_journals,
            "draft": draft_journals,
        },
        "ledger_entries": ledger_count,
        "fiscal_periods": fiscal_periods,
        "recent_audit_log": recent_audit,
        "activity_last_7_days": activity_last_7_days,
    }
