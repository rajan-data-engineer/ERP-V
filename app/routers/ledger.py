from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.ledger import Ledger
from app.dependencies.auth_dependency import require_role

router = APIRouter(prefix="/ledger", tags=["Ledger"])

@router.get("/")
def get_ledger(
    account_id: int = None,
    journal_id: str = None,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    query = select(Ledger)

    if account_id:
        query = query.where(Ledger.account_id == account_id)
    if journal_id:
        query = query.where(Ledger.journal_id == journal_id)

    result = session.exec(query.order_by(Ledger.effective_date)).all()
    return result
