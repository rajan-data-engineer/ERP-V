from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.core.security import decode_access_token
from app.db.session import get_session
from app.models.user import User

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2),
    session: Session = Depends(get_session)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(401, "Invalid or expired token")

    user = session.exec(select(User).where(User.id == payload["sub"])).first()
    if not user:
        raise HTTPException(404, "User not found")

    if not user.is_active:
        raise HTTPException(403, "Account pending admin approval")

    return user
