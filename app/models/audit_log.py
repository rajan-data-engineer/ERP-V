from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: Optional[int] = None
    action: str
    details: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
