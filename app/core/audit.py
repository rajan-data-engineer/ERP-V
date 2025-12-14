from starlette.middleware.base import BaseHTTPMiddleware
from app.db.session import get_session
from app.models.audit_log import AuditLog
from app.dependencies.auth_dependency import decode_token
from sqlmodel import Session
from datetime import datetime

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        session_gen = get_session()
        session: Session = next(session_gen)

        user_id = None
        token = request.headers.get("Authorization", "").replace("Bearer ", "")

        payload = decode_token(token) if token else None
        if payload:
            user_id = payload.get("sub")

        response = await call_next(request)

        log = AuditLog(
            user_id=user_id,
            action=f"{request.method} {request.url.path}",
            details=response.status_code,
            timestamp=datetime.utcnow()
        )
        session.add(log)
        session.commit()

        return response
