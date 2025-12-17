from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies.auth_dependency import require_role, get_current_user
from app.services.accounting_service import AccountingService

router = APIRouter(prefix="/journal", tags=["Journals"])


# --------------------------
# CREATE JOURNAL
# --------------------------
@router.post("/create")
def create_journal(
    description: str,
    effective_date: str,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    return AccountingService.create_journal(description, user.id, effective_date, session)


# --------------------------
# ADD LINE
# --------------------------
@router.post("/line/{journal_id}")
def add_line(
    journal_id: int,
    account_id: int,
    debit: float,
    credit: float,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    return AccountingService.add_line(journal_id, account_id, debit, credit, session)


# --------------------------
# POST JOURNAL
# --------------------------
@router.post("/post/{journal_id}")
def post_journal(
    journal_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    return AccountingService.post_journal(journal_id, user.id, session)


# --------------------------
# CANCEL JOURNAL
# --------------------------
@router.post("/cancel/{journal_id}")
def cancel_journal(
    journal_id: int,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    try:
        return AccountingService.cancel_journal(journal_id, user.id, session)
    except Exception as e:
        raise HTTPException(400, str(e))


# --------------------------
# LIST JOURNALS
# --------------------------
@router.get("/")
def list_journals(
    status: str = None,
    date_from: str = None,
    date_to: str = None,
    search: str = None,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    return AccountingService.list_journals(session, status, date_from, date_to, search)


# --------------------------
# JOURNAL DETAIL
# --------------------------
@router.get("/{journal_id}")
def journal_detail(
    journal_id: int,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    try:
        return AccountingService.journal_detail(journal_id, session)
    except Exception as e:
        raise HTTPException(404, str(e))
