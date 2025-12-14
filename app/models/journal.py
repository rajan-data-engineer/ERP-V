from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class JournalEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    journal_id: str = Field(index=True)        # Unique string
    memo: Optional[str] = None
    description: Optional[str] = None

    fiscal_period_id: Optional[int] = Field(default=None, foreign_key="fiscalperiod.id")

    entry_date: datetime = Field(default_factory=datetime.utcnow)
    effective_date: datetime = Field(default_factory=datetime.utcnow)

    created_by: Optional[int] = None
    approved_by: Optional[int] = None
    posted_by: Optional[int] = None

    status: str = Field(default="draft")  
    # draft, submitted, approved, posted, cancelled


class JournalLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    journal_entry_id: int = Field(foreign_key="journalentry.id")
    account_id: int = Field(foreign_key="account.id")

    debit: float = 0.0
    credit: float = 0.0

    line_memo: Optional[str] = None
