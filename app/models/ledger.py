from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Ledger(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    journal_id: str = Field(foreign_key="journal.id")
    account_id: int

    debit: float = 0.0
    credit: float = 0.0

    effective_date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
