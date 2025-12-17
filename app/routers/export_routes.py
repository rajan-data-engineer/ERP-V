from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies.auth_dependency import require_role
from app.services.excel_export_service import ExcelExportService

EXPORT_DIR = "app/exports"

router = APIRouter(prefix="/export", tags=["Export"])


@router.get("/trial_balance")
def export_tb(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    filename = ExcelExportService.export_trial_balance(session)
    return FileResponse(f"{EXPORT_DIR}/{filename}", filename=filename)


@router.get("/ledger")
def export_ledger(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    filename = ExcelExportService.export_ledger(session)
    return FileResponse(f"{EXPORT_DIR}/{filename}", filename=filename)


@router.get("/journals")
def export_journals(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    filename = ExcelExportService.export_journals(session)
    return FileResponse(f"{EXPORT_DIR}/{filename}", filename=filename)


@router.get("/accounts")
def export_accounts(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    filename = ExcelExportService.export_chart_of_accounts(session)
    return FileResponse(f"{EXPORT_DIR}/{filename}", filename=filename)


@router.get("/audit")
def export_audit(
    session: Session = Depends(get_session),
    user=Depends(require_role("admin"))
):
    filename = ExcelExportService.export_audit_logs(session)
    return FileResponse(f"{EXPORT_DIR}/{filename}", filename=filename)
