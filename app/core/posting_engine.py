# app/core/posting_engine.py

from sqlmodel import Session, select

from app.models.journal import JournalEntry, JournalLine
from app.models.ledger import LedgerEntry
from app.core.audit import log_event
from app.services.fiscal_service import FiscalService


def post_journal(journal_id: int, user_id: int, session: Session):

    journal = session.get(JournalEntry, journal_id)
    if not journal:
        raise ValueError("Journal entry not found.")
# Validate fiscal period
FiscalService.validate_posting_date(journal.effective_date, session)

    if journal.status == "posted":
        raise ValueError("Journal entry already posted.")

    # Fetch lines
    lines = session.exec(
        select(JournalLine).where(JournalLine.journal_id == journal_id)
    ).all()

    if not lines:
        raise ValueError("Journal entry has no lines.")

    # Validate double-entry balance
    debit_total = sum(l.debit for l in lines)
    credit_total = sum(l.credit for l in lines)

    if debit_total != credit_total:
        raise ValueError("Journal is unbalanced (DR != CR).")

    # Create ledger entries
    for line in lines:
        ledger = LedgerEntry(
            journal_id=journal.id,
            account_id=line.account_id,
            debit=line.debit,
            credit=line.credit,
            effective_date=journal.effective_date,
        )
        session.add(ledger)

    journal.status = "posted"
    session.add(journal)
    session.commit()

    log_event("journal_posted", user_id, f"Journal {journal_id} posted", session)

    return True
