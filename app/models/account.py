from sqlmodel import SQLModel, Field
from typing import Optional

class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    account_number: str = Field(index=True)
    account_name: str

    fsli_code: Optional[str] = None      # Financial Statement Line Item
    category: str                        # Asset, Liability, Equity, Revenue, Expense

    is_active: bool = Field(default=True)
