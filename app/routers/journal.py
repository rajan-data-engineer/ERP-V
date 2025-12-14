from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.accounting import JournalEntry, JournalLine
from app.dependencies.auth_dependency import get_current_user
from app.services.accounting_engine import (
    generate_journal_id,
    validate_balanced,
    log_action
)

router = APIRouter(prefix="/journal", tags=["Journal"])


# --------------------------------------
# Create Journal (DRAFT)
# --------------------------------------
@router.post("/create")
def create_journal(data: dict, user=Depends(get_current_user), session: Session = Depends(get_session)):
    lines = data.get("lines", [])
    if not lines:
        raise HTTPException(400, "Journal requires lines.")

    # Convert line dicts → JournalLine objects
    line_objs = [JournalLine(**line) for line in lines]

    if not validate_balanced(line_objs):
        raise HTTPException(400, "Journal is not balanced (DR != CR).")

    journal_id = generate_journal_id(session)

    entry = JournalEntry(
        journal_id=journal_id,
        description=data.get("description"),
        fiscal_year=datetime.utcnow().year,
        fiscal_period=datetime.utcnow().month,
        created_by=user.id,
        effective_date=data.get("effective_date"),
    )

    session.add(entry)
    session.commit()
    session.refresh(entry)

    # Assign journal_entry_id to lines
    for line in line_objs:
        line.journal_entry_id = entry.id
        session.add(line)

    session.commit()

    log_action(session, user.id, "CREATE_JOURNAL", "journal", entry.id)

    return {"message": "Journal created", "journal_id": journal_id, "id": entry.id}


# --------------------------------------
# POST (LOCK) Journal
# --------------------------------------
@router.post("/post/{journal_id}")
def post_journal(journal_id: int, user=Depends(get_current_user), session: Session = Depends(get_session)):
    
    entry = session.get(JournalEntry, journal_id)
    if not entry:
        raise HTTPException(404, "Journal not found")

    if entry.status == "posted":
        raise HTTPException(400, "Already posted")

    entry.status = "posted"
    entry.approved_by = user.id
    entry.updated_at = datetime.utcnow()

    session.add(entry)
    session.commit()

    log_action(session, user.id, "POST_JOURNAL", "journal", entry.id)

    return {"message": "Journal posted", "id": entry.id}


# --------------------------------------
# Cancel Journal
# --------------------------------------
@router.post("/cancel/{journal_id}")
def cancel(journal_id: int, user=Depends(get_current_user), session: Session = Depends(get_session)):
    entry = session.get(JournalEntry, journal_id)

    if not entry:
        raise HTTPException(404, "Journal not found")

    entry.status = "cancelled"
    entry.modified_by = user.id

    session.add(entry)
    session.commit()

    log_action(session, user.id, "CANCEL_JOURNAL", "journal", entry.id)

    return {"message": "Journal cancelled"}
