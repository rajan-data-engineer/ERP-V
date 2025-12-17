from sqlmodel import Session, select
from datetime import datetime
from typing import Optional, List, Dict

from app.models.audit_log import AuditLog


class AuditLogService:

    # ---------------------------------------------
    # CORE FILTER FUNCTION
    # ---------------------------------------------
    @staticmethod
    def list_logs(
        session: Session,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 200,
        offset: int = 0
    ) -> List[AuditLog]:

        query = select(AuditLog)

        if user_id:
            query = query.where(AuditLog.user_id == user_id)

        if action:
            query = query.where(AuditLog.action == action)

        if date_from:
            df = datetime.fromisoformat(date_from)
            query = query.where(AuditLog.timestamp >= df)

        if date_to:
            dt = datetime.fromisoformat(date_to)
            query = query.where(AuditLog.timestamp <= dt)

        if search:
            query = query.where(AuditLog.details.ilike(f"%{search}%"))

        query = query.order_by(AuditLog.timestamp.desc())
        query = query.offset(offset).limit(limit)

        return session.exec(query).all()

    # ---------------------------------------------
    # DISTINCT ACTION TYPES
    # ---------------------------------------------
    @staticmethod
    def list_actions(session: Session) -> List[str]:
        rows = session.exec(select(AuditLog.action)).all()
        return sorted(list({row for row, in rows}))

    # ---------------------------------------------
    # EXPORT LOGS (used in Phase 6E)
    # ---------------------------------------------
    @staticmethod
    def export_logs(
        session: Session,
        user_id=None, action=None,
        date_from=None, date_to=None, search=None
    ):
        logs = AuditLogService.list_logs(
            session=session,
            user_id=user_id,
            action=action,
            date_from=date_from,
            date_to=date_to,
            search=search,
            limit=50000,   # export large set
            offset=0
        )

        return [log.dict() for log in logs]
