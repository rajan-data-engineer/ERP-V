from sqlmodel import Field
from datetime import datetime
from typing import Optional

class TimestampMixin:
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class StatusMixin:
    status: str = Field(default="draft")  # draft, posted, cancelled
