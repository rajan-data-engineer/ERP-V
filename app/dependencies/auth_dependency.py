from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.core.config import get_settings
from app.core.security import decode_access_token
from app.db.session import get_session
from app.models.user import User

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(401, "Invalid or expired token")

    user = session.exec(select(User).where(User.id == payload["sub"])).first()

    if not user:
        raise HTTPException(404, "User not found")

    return user


def require_role(*allowed_roles):
    def checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(403, "Not permitted")
        return user
    return checker
