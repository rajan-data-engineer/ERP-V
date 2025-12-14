# app/services/accounting_service.py

from sqlmodel import Session, select
from datetime import datetime

from app.models.journal import JournalEntry, JournalLine
from app.models.ledger import LedgerEntry
from app.core.posting_engine import post_journal
from app.core.audit import log_event


class AccountingService:

    @staticmethod
    def create_journal(description: str, user_id: int, effective_date: datetime, session: Session):
        journal = JournalEntry(
            description=description,
            created_by=user_id,
            effective_date=effective_date,
            status="draft"
        )
        session.add(journal)
        session.commit()
        session.refresh(journal)

        log_event("journal_created", user_id, f"Journal {journal.id} created", session)

        return journal

    @staticmethod
    def add_line(journal_id: int, account_id: int, debit: float, credit: float, session: Session):
        line = JournalLine(
            journal_id=journal_id,
            account_id=account_id,
            debit=debit,
            credit=credit
        )
        session.add(line)
        session.commit()
        session.refresh(line)
        return line

    @staticmethod
    def post_journal(journal_id: int, user_id: int, session: Session):
        post_journal(journal_id, user_id, session)
        return {"message": "Journal posted successfully"}

    @staticmethod
    def get_ledger(account_id: int | None, session: Session):
        query = select(LedgerEntry)

        if account_id:
            query = query.where(LedgerEntry.account_id == account_id)

        result = session.exec(query.order_by(LedgerEntry.effective_date)).all()
        return result
