from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.user import User
from app.core.security import create_access_token
import jwt
from app.core.config import get_settings

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return None

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(401, "Invalid or expired token.")

    user = session.exec(
        select(User).where(User.id == payload["sub"])
    ).first()

    if not user:
        raise HTTPException(404, "User not found.")

    if not user.is_active:
        raise HTTPException(403, "User not approved by admin.")

    return user

def require_role(*allowed_roles):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(403, "Permission denied.")
        return user
    return wrapper
