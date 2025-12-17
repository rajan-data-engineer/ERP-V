from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies.auth_dependency import require_role
from app.services.account_hierarchy_service import AccountHierarchyService
from app.services.accounting_service import AccountingService

router = APIRouter(prefix="/accounts", tags=["Account Hierarchy"])


@router.get("/tree")
def account_tree(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    return AccountHierarchyService.build_tree(session)


@router.get("/tree/balances")
def account_tree_with_balances(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    return AccountHierarchyService.build_tree_with_balances(session)


@router.get("/tree/financials")
def account_tree_financials(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    return {
        "trial_balance": AccountingService.trial_balance_tree(session),
        "balance_sheet": AccountingService.balance_sheet_tree(session),
        "profit_loss": AccountingService.profit_loss_tree(session)
    }
