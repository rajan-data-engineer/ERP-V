from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class ERPBase(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    created_by: Optional[int] = None
    approved_by: Optional[int] = None
    modified_by: Optional[int] = None

    status: str = Field(default="draft")  
    # draft, posted, cancelled, history
