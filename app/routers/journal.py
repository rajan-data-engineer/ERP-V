from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.journal import JournalEntry, JournalLine
from app.models.account import Account
from app.services.accounting_engine import AccountingService
from app.dependencies.auth_dependency import require_role, get_current_user

router = APIRouter(prefix="/journal", tags=["Journal"])

# -----------------------
# Create Journal
# -----------------------
@router.post("/create")
def create_journal(
    description: str,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    journal = JournalEntry(
        journal_id=f"JRN-{int(100000 + journal.id) if False else None}",
        description=description,
        created_by=user.id,
    )
    session.add(journal)
    session.commit()
    session.refresh(journal)

    # Generate readable journal ID
    journal.journal_id = f"JRN-{journal.id:06d}"
    session.add(journal)
    session.commit()

    return journal

# -----------------------
# Add Journal Line
# -----------------------
@router.post("/{journal_id}/line")
def add_line(
    journal_id: int,
    account_id: int,
    debit: float = 0.0,
    credit: float = 0.0,
    memo: str = "",
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    journal = session.get(JournalEntry, journal_id)
    if not journal:
        raise HTTPException(404, "Journal not found.")

    if session.get(Account, account_id) is None:
        raise HTTPException(400, "Account not found.")

    line = JournalLine(
        journal_entry_id=journal_id,
        account_id=account_id,
        debit=debit,
        credit=credit,
        memo=memo
    )

    session.add(line)
    session.commit()
    return {"message": "Line added."}

# -----------------------
# View Journal
# -----------------------
@router.get("/{journal_id}")
def view_journal(
    journal_id: int,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant", "viewer"))
):
    journal = session.get(JournalEntry, journal_id)
    if not journal:
        raise HTTPException(404, "Journal not found.")
    return journal

# -----------------------
# Post Journal
# -----------------------
@router.post("/{journal_id}/post")
def post_journal(
    journal_id: int,
    session: Session = Depends(get_session),
    user=Depends(require_role("admin", "accountant"))
):
    try:
        result = AccountingService.post_journal(session, journal_id, user.id)
        return {"message": "Journal posted.", "journal": result}
    except Exception as e:
        raise HTTPException(400, str(e))
