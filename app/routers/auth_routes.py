from fastapi import APIRouter, Depends, HTTPException, Form
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    existing = session.exec(select(User).where(User.username == username)).first()
    if existing:
        raise HTTPException(400, "Username already exists")

    user = User(
        username=username,
        hashed_password=hash_password(password),
        role="viewer",     # default role
        is_active=False    # requires admin approval
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "User registered successfully. Awaiting admin approval."}


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):

    user = session.exec(select(User).where(User.username == username)).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    if not user.is_active:
        raise HTTPException(403, "Account awaiting admin approval.")

    token = create_access_token({"sub": user.id, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
