# app/routers/journal_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.services.accounting_service import AccountingService
from app.dependencies.auth_dependency import require_role, get_current_user
from app.services.email_service_wrapper import EmailNotifications

router = APIRouter(prefix="/journal", tags=["Journals"])


@router.post("/create")
def create_journal(
    description: str,
    effective_date: str,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    journal = AccountingService.create_journal(description, user.id, effective_date, session)
    return journal


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


@router.post("/post/{journal_id}")
def post_journal(
    journal_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    result = AccountingService.post_journal(journal_id, user.id, session)
    EmailNotifications.notify_admin_journal_posted(journal_id)
    return result
