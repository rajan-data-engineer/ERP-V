# app/db/base.py

from sqlmodel import SQLModel

# Import ALL models so SQLModel knows about them.
from app.models.user import User
from app.models.account import Account
from app.models.journal import JournalEntry, JournalLine
from app.models.ledger import LedgerEntry
from app.models.fiscal import FiscalPeriod
from app.models.audit_log import AuditLog

# This file ensures SQLModel.metadata contains all tables.
__all__ = [
    "User",
    "Account",
    "JournalEntry",
    "JournalLine",
    "LedgerEntry",
    "FiscalPeriod",
    "AuditLog",
]
