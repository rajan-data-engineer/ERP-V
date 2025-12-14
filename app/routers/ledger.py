from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies.auth_dependency import get_current_user
from app.models.accounting import JournalEntry, JournalLine, AuditLog

router = APIRouter(prefix="/ledger", tags=["Ledger"])


@router.get("/journals")
def list_journals(user=Depends(get_current_user), session: Session = Depends(get_session)):
    return session.exec(select(JournalEntry)).all()


@router.get("/journal/{id}")
def journal_detail(id: int, user=Depends(get_current_user), session: Session = Depends(get_session)):
    entry = session.get(JournalEntry, id)
    if not entry:
        return {"error": "Not found"}

    lines = session.exec(
        select(JournalLine).where(JournalLine.journal_entry_id == id)
    ).all()

    return {"entry": entry, "lines": lines}


@router.get("/audit")
def audit_logs(user=Depends(get_current_user), session: Session = Depends(get_session)):
    return session.exec(select(AuditLog)).all()
