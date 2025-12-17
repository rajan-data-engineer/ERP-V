# app/core/audit.py

from datetime import datetime
from sqlmodel import Session

from app.db.session import get_session
from app.models.audit_log import AuditLog


def log_event(action: str, user_id: int, details: str, session: Session | None = None):
    """
    Create an audit trail entry.
    Automatically opens/closes a DB session if not supplied.
    """

    close_session = False
    if session is None:
        session = next(get_session())   # open new session safely
        close_session = True

    entry = AuditLog(
        action=action,
        user_id=user_id,
        details=details,
        timestamp=datetime.utcnow(),
    )

    session.add(entry)
    session.commit()

    if close_session:
        session.close()

    return entry.id
