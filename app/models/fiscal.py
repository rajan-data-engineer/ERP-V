from sqlmodel import SQLModel, Field
from datetime import date, datetime
from typing import Optional


# ------------------------------
# Common Mixins
# ------------------------------
class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class StatusMixin(SQLModel):
    status: str = Field(default="draft")  # draft, posted, cancelled


# ------------------------------
# Fiscal Period Model
# ------------------------------
class FiscalPeriod(SQLModel, table=True):
    """
    Example:
    name = "2025-01"
    start_date = 2025-01-01
    end_date = 2025-01-31
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    start_date: date
    end_date: date
    is_closed: bool = False
