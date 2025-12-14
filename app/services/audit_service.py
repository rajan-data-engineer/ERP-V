from sqlmodel import Session
from app.models.audit_log import AuditLog

class AuditService:

    @staticmethod
    def log(session: Session, user_id: int, action: str, details: str = ""):
        entry = AuditLog(
            user_id=user_id,
            action=action,
            details=details
        )
        session.add(entry)
        session.commit()
