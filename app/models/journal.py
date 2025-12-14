from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class JournalEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    description: str
    created_by: int
    effective_date: datetime = Field(default_factory=datetime.utcnow)

    status: str = Field(default="draft")  # draft, posted, cancelled

    lines: List["JournalLine"] = Relationship(back_populates="journal")


class JournalLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    journal_id: int = Field(foreign_key="journalentry.id")
    account_id: int = Field(foreign_key="account.id")

    debit: float = 0.0
    credit: float = 0.0

    journal: Optional[JournalEntry] = Relationship(back_populates="lines")
