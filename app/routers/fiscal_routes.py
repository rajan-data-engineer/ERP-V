from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies.auth_dependency import require_role
from app.services.fiscal_service import FiscalService

router = APIRouter(prefix="/fiscal", tags=["Fiscal Periods"])


@router.post("/create")
def create_period(
    fiscal_year: int,
    period_number: int,
    start_date: str,
    end_date: str,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin"))
):
    try:
        return FiscalService.create_period(
            fiscal_year, period_number, start_date, end_date, session
        )
    except Exception as e:
        raise HTTPException(400, str(e))


@router.get("/")
def list_periods(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    return FiscalService.list_periods(session)


@router.post("/close/{period_id}")
def close_period(
    period_id: int,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin"))
):
    try:
        return FiscalService.close_period(period_id, session)
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/open/{period_id}")
def open_period(
    period_id: int,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin"))
):
    try:
        return FiscalService.open_period(period_id, session)
    except Exception as e:
        raise HTTPException(400, str(e))
