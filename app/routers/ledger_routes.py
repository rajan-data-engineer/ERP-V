# app/routers/ledger_routes.py

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies.auth_dependency import require_role
from app.services.accounting_service import AccountingService

router = APIRouter(prefix="/ledger", tags=["Ledger"])


@router.get("/")
def get_ledger(
    account_id: int | None = None,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    return AccountingService.get_ledger(account_id, session)
