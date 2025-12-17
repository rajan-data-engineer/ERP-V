from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies.auth_dependency import require_role
from app.services.accounting_service import AccountingService

router = APIRouter(prefix="/ledger", tags=["Ledger"])


# --------------------------
# LEDGER LIST
# --------------------------
@router.get("/")
def get_ledger(
    account_id: int | None = None,
    date_from: str = None,
    date_to: str = None,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    return AccountingService.get_ledger(account_id, session, date_from, date_to)


# --------------------------
# TRIAL BALANCE
# --------------------------
@router.get("/trial_balance")
def trial_balance(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    return AccountingService.trial_balance(session)


# --------------------------
# BALANCE SHEET
# --------------------------
@router.get("/balance_sheet")
def balance_sheet(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    return AccountingService.balance_sheet(session)


# --------------------------
# PROFIT AND LOSS
# --------------------------
@router.get("/profit_loss")
def profit_loss(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    return AccountingService.profit_loss(session)
