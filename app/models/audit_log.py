from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action: str = Field(max_length=100)      # concise event label
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    details: str = Field(max_length=2000)    # prevents runaway logs
