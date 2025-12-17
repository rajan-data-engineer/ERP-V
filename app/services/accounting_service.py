from sqlmodel import Session, select, func
from datetime import datetime
from typing import List, Optional, Dict

from app.models.journal import JournalEntry, JournalLine
from app.models.ledger import LedgerEntry
from app.models.account import Account
from app.core.audit import log_event
from app.core.posting_engine import post_journal


class AccountingService:

    # ----------------------------------------
    # JOURNAL CREATION
    # ----------------------------------------
    @staticmethod
    def create_journal(description: str, user_id: int, effective_date: str, session: Session):
        journal = JournalEntry(
            description=description,
            created_by=user_id,
            effective_date=datetime.fromisoformat(effective_date),
            status="draft"
        )
        session.add(journal)
        session.commit()
        session.refresh(journal)

        log_event("journal_created", user_id, f"Journal {journal.id} created", session)
        return journal

    @staticmethod
    def add_line(journal_id: int, account_id: int, debit: float, credit: float, session: Session):
        line = JournalLine(
            journal_id=journal_id,
            account_id=account_id,
            debit=debit,
            credit=credit
        )
        session.add(line)
        session.commit()
        session.refresh(line)
        return line

    @staticmethod
    def post_journal(journal_id: int, user_id: int, session: Session):
        post_journal(journal_id, user_id, session)
        return {"message": "Journal posted successfully"}

    @staticmethod
    def cancel_journal(journal_id: int, user_id: int, session: Session):
        journal = session.get(JournalEntry, journal_id)

        if not journal:
            raise ValueError("Journal not found.")

        if journal.status == "posted":
            raise ValueError("Posted journals cannot be cancelled.")

        journal.status = "cancelled"
        session.commit()

        log_event("journal_cancelled", user_id, f"Journal {journal_id} cancelled", session)

        return {"message": f"Journal {journal_id} cancelled"}

    # ----------------------------------------
    # JOURNAL QUERIES
    # ----------------------------------------
    @staticmethod
    def list_journals(
        session: Session,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        search: Optional[str] = None
    ):
        query = select(JournalEntry)

        if status:
            query = query.where(JournalEntry.status == status)

        if date_from:
            df = datetime.fromisoformat(date_from)
            query = query.where(JournalEntry.effective_date >= df)

        if date_to:
            dt = datetime.fromisoformat(date_to)
            query = query.where(JournalEntry.effective_date <= dt)

        if search:
            query = query.where(JournalEntry.description.ilike(f"%{search}%"))

        return session.exec(query.order_by(JournalEntry.effective_date)).all()

    @staticmethod
    def journal_detail(journal_id: int, session: Session):
        journal = session.get(JournalEntry, journal_id)
        if not journal:
            raise ValueError("Journal not found.")

        lines = session.exec(
            select(JournalLine).where(JournalLine.journal_id == journal_id)
        ).all()

        return {
            "journal": journal,
            "lines": lines
        }

    # ----------------------------------------
    # LEDGER / TRIAL BALANCE / FINANCIALS
    # ----------------------------------------
    @staticmethod
    def get_ledger(account_id: int | None, session: Session,
                   date_from: Optional[str] = None,
                   date_to: Optional[str] = None):

        query = select(LedgerEntry)

        if account_id:
            query = query.where(LedgerEntry.account_id == account_id)

        if date_from:
            df = datetime.fromisoformat(date_from)
            query = query.where(LedgerEntry.effective_date >= df)

        if date_to:
            dt = datetime.fromisoformat(date_to)
            query = query.where(LedgerEntry.effective_date <= dt)

        return session.exec(query.order_by(LedgerEntry.effective_date)).all()

    # ----------------------------------------
    # TRIAL BALANCE
    # ----------------------------------------
    @staticmethod
    def trial_balance(session: Session):
        accounts = session.exec(select(Account)).all()
        ledger = session.exec(select(LedgerEntry)).all()

        tb = {}

        for acc in accounts:
            tb[acc.id] = {
                "account_id": acc.id,
                "code": acc.code,
                "name": acc.name,
                "type": acc.type,
                "debit": 0,
                "credit": 0,
                "closing_balance": 0
            }

        for entry in ledger:
            tb_entry = tb[entry.account_id]
            tb_entry["debit"] += entry.debit
            tb_entry["credit"] += entry.credit

        # Closing balance = DR - CR for asset/expense
        # Closing balance = CR - DR for liability/equity/income
        for acc in accounts:
            row = tb[acc.id]
            if acc.type in ["asset", "expense"]:
                row["closing_balance"] = row["debit"] - row["credit"]
            else:
                row["closing_balance"] = row["credit"] - row["debit"]

        return list(tb.values())

    # ----------------------------------------
    # BALANCE SHEET
    # ----------------------------------------
    @staticmethod
    def balance_sheet(session: Session):
        tb = AccountingService.trial_balance(session)

        sheet = {
            "assets": [],
            "liabilities": [],
            "equity": [],
            "total_assets": 0,
            "total_liabilities": 0,
            "total_equity": 0
        }

        for row in tb:
            if row["type"] == "asset":
                sheet["assets"].append(row)
                sheet["total_assets"] += row["closing_balance"]

            if row["type"] == "liability":
                sheet["liabilities"].append(row)
                sheet["total_liabilities"] += row["closing_balance"]

            if row["type"] == "equity":
                sheet["equity"].append(row)
                sheet["total_equity"] += row["closing_balance"]

        return sheet

    # ----------------------------------------
    # PROFIT AND LOSS
    # ----------------------------------------
    @staticmethod
    def profit_loss(session: Session):
        tb = AccountingService.trial_balance(session)

        income = []
        expense = []
        total_income = 0
        total_expense = 0

        for row in tb:
            if row["type"] == "income":
                income.append(row)
                total_income += row["closing_balance"]

            if row["type"] == "expense":
                expense.append(row)
                total_expense += row["closing_balance"]

        return {
            "income": income,
            "expense": expense,
            "total_income": total_income,
            "total_expense": total_expense,
            "net_profit": total_income - total_expense
        }
 