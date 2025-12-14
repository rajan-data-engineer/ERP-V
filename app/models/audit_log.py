from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action: str
    user_id: Optional[int] = None
    details: str
