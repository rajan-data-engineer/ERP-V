from datetime import datetime
from sqlmodel import Session, select

from app.models.accounting import JournalEntry, JournalLine, AuditLog


# ---------------------------------------
# Generate Journal ID: JRN-YYYY-XXXX
# ---------------------------------------
def generate_journal_id(session: Session) -> str:
    year = datetime.utcnow().year

    last = session.exec(
        select(JournalEntry).where(JournalEntry.fiscal_year == year)
    ).all()

    number = len(last) + 1
    return f"JRN-{year}-{number:04d}"


# ---------------------------------------
# Validate DR = CR
# ---------------------------------------
def validate_balanced(lines):
    debit_total = sum(line.debit for line in lines)
    credit_total = sum(line.credit for line in lines)
    return debit_total == credit_total


# ---------------------------------------
# Audit Logging
# ---------------------------------------
def log_action(session: Session, user_id: int, action: str, target: str, target_id: int, details: str = ""):
    log = AuditLog(
        user_id=user_id,
        action=action,
        target=target,
        target_id=target_id,
        details=details
    )
    session.add(log)
    session.commit()
