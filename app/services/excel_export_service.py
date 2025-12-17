import os
from datetime import datetime
from sqlmodel import Session

from openpyxl import Workbook

from app.services.accounting_service import AccountingService
from app.services.audit_log_service import AuditLogService
from app.models.journal import JournalEntry, JournalLine
from app.models.ledger import LedgerEntry
from app.models.account import Account

EXPORT_DIR = "app/exports"


class ExcelExportService:

    @staticmethod
    def _create_workbook(headers, rows):
        wb = Workbook()
        ws = wb.active

        # Write headers
        ws.append(headers)

        # Write rows
        for r in rows:
            ws.append(r)

        return wb

    @staticmethod
    def _save_workbook(wb, filename):
        if not os.path.exists(EXPORT_DIR):
            os.makedirs(EXPORT_DIR)

        path = os.path.join(EXPORT_DIR, filename)
        wb.save(path)
        return filename

    # -------------------------------------------------------
    # TRIAL BALANCE EXPORT
    # -------------------------------------------------------
    @staticmethod
    def export_trial_balance(session: Session):
        tb = AccountingService.trial_balance(session)

        headers = ["Account Code", "Account Name", "Type",
                   "Debit", "Credit", "Closing Balance"]

        rows = []
        for row in tb:
            rows.append([
                row["code"],
                row["name"],
                row["type"],
                row["debit"],
                row["credit"],
                row["closing_balance"],
            ])

        wb = ExcelExportService._create_workbook(headers, rows)
        filename = f"trial_balance_{datetime.utcnow().isoformat()}.xlsx"
        return ExcelExportService._save_workbook(wb, filename)

    # -------------------------------------------------------
    # GENERAL LEDGER EXPORT
    # -------------------------------------------------------
    @staticmethod
    def export_ledger(session: Session):
        ledger = session.exec(select(LedgerEntry)).all()

        headers = [
            "Journal ID", "Account ID", "Debit", "Credit",
            "Effective Date"
        ]

        rows = []
        for e in ledger:
            rows.append([
                e.journal_id,
                e.account_id,
                e.debit,
                e.credit,
                e.effective_date.isoformat()
            ])

        wb = ExcelExportService._create_workbook(headers, rows)
        filename = f"ledger_{datetime.utcnow().isoformat()}.xlsx"
        return ExcelExportService._save_workbook(wb, filename)

    # -------------------------------------------------------
    # JOURNAL ENTRIES EXPORT
    # -------------------------------------------------------
    @staticmethod
    def export_journals(session: Session):
        journals = session.exec(select(JournalEntry)).all()

        headers = [
            "Journal ID", "Description", "Status",
            "Effective Date", "Created At", "Created By"
        ]

        rows = []
        for j in journals:
            rows.append([
                j.id,
                j.description,
                j.status,
                j.effective_date.isoformat(),
                j.created_at.isoformat() if j.created_at else "",
                j.created_by
            ])

        wb = ExcelExportService._create_workbook(headers, rows)
        filename = f"journals_{datetime.utcnow().isoformat()}.xlsx"
        return ExcelExportService._save_workbook(wb, filename)

    # -------------------------------------------------------
    # CHART OF ACCOUNTS EXPORT
    # -------------------------------------------------------
    @staticmethod
    def export_chart_of_accounts(session: Session):
        accounts = session.exec(select(Account)).all()

        headers = ["Account ID", "Code", "Name", "Type", "Parent ID"]

        rows = []
        for acc in accounts:
            rows.append([
                acc.id,
                acc.code,
                acc.name,
                acc.type,
                acc.parent_id
            ])

        wb = ExcelExportService._create_workbook(headers, rows)
        filename = f"chart_of_accounts_{datetime.utcnow().isoformat()}.xlsx"
        return ExcelExportService._save_workbook(wb, filename)

    # -------------------------------------------------------
    # AUDIT LOG EXPORT
    # -------------------------------------------------------
    @staticmethod
    def export_audit_logs(session: Session):
        logs = AuditLogService.export_logs(session)

        headers = ["ID", "Timestamp", "User ID", "Action", "Details"]

        rows = []
        for log in logs:
            rows.append([
                log["id"],
                log["timestamp"],
                log["user_id"],
                log["action"],
                log["details"],
            ])

        wb = ExcelExportService._create_workbook(headers, rows)
        filename = f"audit_logs_{datetime.utcnow().isoformat()}.xlsx"
        return ExcelExportService._save_workbook(wb, filename)
