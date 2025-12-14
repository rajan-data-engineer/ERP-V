from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(index=True, unique=True)
    hashed_password: str

    role: str = Field(default="viewer")  # viewer, accountant, admin
    is_active: bool = Field(default=False)  # Requires admin approval

    email: Optional[str] = None
