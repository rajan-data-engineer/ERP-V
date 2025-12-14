from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.logger import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ------------------------------
# REGISTER USER (Needs Admin Approval)
# ------------------------------
@router.post("/register")
def register(
    username: str,
    email: str,
    password: str,
    session: Session = Depends(get_session)
):
    existing = session.exec(
        select(User).where(
            (User.username == username) | 
            (User.email == email)
        )
    ).first()

    if existing:
        raise HTTPException(400, "Username or email already taken.")

    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role="viewer",
        is_active=False
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    logger.info(f"New user registered (pending approval): {username}")

    return {"message": "Registration successful. Waiting for admin approval."}


# ------------------------------
# LOGIN
# ------------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Invalid username or password.")

    if not user.is_active:
        raise HTTPException(403, "User not approved yet.")

    token = create_access_token({"sub": user.id, "role": user.role})

    return {"access_token": token, "token_type": "bearer"}


# ------------------------------
# PROFILE
# ------------------------------
@router.get("/me")
def me(user: User = Depends(lambda: None), session: Session = Depends(get_session)):
    # Me endpoint handled via auth_dependency in actual usage
    return {"status": "ok"}
