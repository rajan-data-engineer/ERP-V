from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(index=True, unique=True)
    email: Optional[str] = Field(default=None, index=True)
    password_hash: str

    role: str = Field(default="viewer")       # admin / viewer / accountant / inventory_manager...
    is_active: bool = Field(default=False)    # Requires admin approval
    created_at: datetime = Field(default_factory=datetime.utcnow)
    approved_at: Optional[datetime] = None
