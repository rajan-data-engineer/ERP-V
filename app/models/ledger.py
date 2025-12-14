from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class LedgerEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    journal_id: int = Field(foreign_key="journalentry.id")
    account_id: int = Field(foreign_key="account.id")

    debit: float = 0.0
    credit: float = 0.0

    effective_date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
