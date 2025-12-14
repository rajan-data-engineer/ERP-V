# app/routers/auth_routes.py

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.services.email_service_wrapper import EmailNotifications

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(""),
    session: Session = Depends(get_session)
):
    existing = session.exec(select(User).where(User.username == username)).first()
    if existing:
        raise HTTPException(400, "Username already exists")

    user = User(
        username=username,
        hashed_password=hash_password(password),
        email=email,
        role="viewer",
        is_active=False
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    EmailNotifications.notify_admin_new_user(username)

    return {"message": "Registration received. Await admin approval."}


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.username == username)).first()

    if not user or not verify_password(password, user.hashed_password):
        EmailNotifications.notify_admin_failed_login(username)
        raise HTTPException(401, "Invalid credentials")

    if not user.is_active:
        raise HTTPException(403, "Account awaiting admin approval")

    token = create_access_token({"sub": user.id, "role": user.role})

    return {"access_token": token, "token_type": "bearer"}
