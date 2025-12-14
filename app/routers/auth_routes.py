from fastapi import APIRouter, Depends, HTTPException, Form
from sqlmodel import Session, select
from app.db.session import get_session
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(None),
    session: Session = Depends(get_session)
):
    exists = session.exec(select(User).where(User.username == username)).first()
    if exists:
        raise HTTPException(400, "Username already exists")

    user = User(
        username=username,
        password_hash=hash_password(password),
        email=email,
        role="viewer",
        is_active=False   # Requires admin approval
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "Registration submitted. Await admin approval."}


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(400, "Invalid username or password")

    if not verify_password(password, user.password_hash):
        raise HTTPException(400, "Invalid username or password")

    if not user.is_active:
        raise HTTPException(403, "User not approved by admin")

    token = create_access_token({"sub": user.id, "role": user.role})

    return {"access_token": token, "token_type": "bearer"}
