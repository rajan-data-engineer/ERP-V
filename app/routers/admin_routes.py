from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime

from app.db.session import get_session
from app.dependencies.auth_dependency import get_current_user
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admin access required")
    return user


@router.get("/pending")
def list_pending_users(
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    return session.exec(select(User).where(User.is_active == False)).all()


@router.post("/approve/{user_id}")
def approve_user(
    user_id: int,
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.is_active = True
    user.approved_at = datetime.utcnow()

    session.add(user)
    session.commit()

    return {"message": f"User {user.username} approved"}
