# app/routers/account_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.account import Account
from app.db.session import get_session
from app.dependencies.auth_dependency import require_role

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/")
def create_account(
    account: Account,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.get("/")
def list_accounts(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    return session.exec(select(Account)).all()
