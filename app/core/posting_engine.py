from sqlmodel import Session, select
from app.models.journal import JournalEntry, JournalLine
from app.models.ledger import Ledger
from app.models.fiscal import FiscalPeriod
from app.models.audit_log import AuditLog
from datetime import datetime

class PostingError(Exception):
    pass

class PostingEngine:

    @staticmethod
    def validate_balanced(lines: list[JournalLine]):
        total_debit = sum(l.debit for l in lines)
        total_credit = sum(l.credit for l in lines)

        if round(total_debit, 2) != round(total_credit, 2):
            raise PostingError("Journal is not balanced (Debits != Credits).")

    @staticmethod
    def check_fiscal_period(session: Session, date: datetime):
        fiscal = session.exec(
            select(FiscalPeriod).where(
                (FiscalPeriod.fiscal_year == date.year) &
                (FiscalPeriod.fiscal_month == date.month)
            )
        ).first()

        if not fiscal or not fiscal.is_open:
            raise PostingError("Fiscal period is closed.")

    @staticmethod
    def post_journal(session: Session, journal_id: int, user_id: int):
        journal = session.get(JournalEntry, journal_id)
        if not journal:
            raise PostingError("Journal not found.")

        if journal.status == "posted":
            raise PostingError("Journal already posted.")

        # Validate balance
        PostingEngine.validate_balanced(journal.lines)

        # Check fiscal period
        PostingEngine.check_fiscal_period(session, journal.effective_date)

        # Post to ledger
        for line in journal.lines:
            entry = Ledger(
                journal_id=journal.journal_id,
                account_id=line.account_id,
                debit=line.debit,
                credit=line.credit,
                effective_date=journal.effective_date,
            )
            session.add(entry)

        journal.status = "posted"
        journal.approved_by = user_id

        # Audit log
        audit = AuditLog(
            user_id=user_id,
            action="POST_JOURNAL",
            details=f"Journal {journal.journal_id} posted."
        )
        session.add(audit)

        session.commit()

        return journal
