from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class FiscalPeriod(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    fiscal_year: int
    period_number: int  # 1–12
    start_date: date
    end_date: date

    is_closed: bool = Field(default=False)
