from fastapi import APIRouter, Depends, HTTPException, Form
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.user import User
from app.core.security import create_access_token
from app.core.config import get_settings
from passlib.context import CryptContext

settings = get_settings()
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    exists = session.exec(select(User).where(User.username == username)).first()
    if exists:
        raise HTTPException(400, "User already exists")

    user = User(
        username=username,
        password_hash=pwd.hash(password),
        role="viewer",
        is_active=False
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "User registered. Await admin approval."}


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.username == username)).first()

    if not user or not pwd.verify(password, user.password_hash):
        raise HTTPException(400, "Invalid username or password")

    if not user.is_active:
        raise HTTPException(403, "Awaiting admin approval")

    token = create_access_token({"sub": user.id, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
