from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    user_id: Optional[int] = Field(default=None)
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[str] = None
