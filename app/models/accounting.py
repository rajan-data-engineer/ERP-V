from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


# -----------------------------
# Journal Entry (Header)
# -----------------------------
class JournalEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    journal_id: str = Field(index=True, unique=True)
    description: Optional[str] = None

    entry_date: datetime = Field(default_factory=datetime.utcnow)
    effective_date: Optional[datetime] = None

    status: str = Field(default="draft")  # draft, posted, cancelled

    fiscal_year: Optional[int] = None
    fiscal_period: Optional[int] = None

    created_by: Optional[int] = None
    approved_by: Optional[int] = None
    modified_by: Optional[int] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    lines: List["JournalLine"] = Relationship(back_populates="entry")


# -----------------------------
# Journal Lines (Debit/Credit)
# -----------------------------
class JournalLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    journal_entry_id: int = Field(foreign_key="journalentry.id")
    account_number: str
    account_name: str

    debit: float = 0.0
    credit: float = 0.0
    memo: Optional[str] = None
    user_id: Optional[int] = None

    entry: JournalEntry = Relationship(back_populates="lines")


# -----------------------------
# Audit Log
# -----------------------------
class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = None
    action: str
    target: str
    target_id: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[str] = None  # JSON or text
