from datetime import datetime
from sqlmodel import Session
from app.core.config import get_settings
from app.db.session import get_session
from app.models.audit_log import AuditLog

settings = get_settings()


def log_event(action: str, user_id: int, details: str, session: Session | None = None):

    close_session = False
    if session is None:
        session = get_session()
        close_session = True

    entry = AuditLog(
        timestamp=datetime.utcnow(),
        action=action,
        user_id=user_id,
        details=details
    )

    session.add(entry)
    session.commit()

    if close_session:
        session.close()
