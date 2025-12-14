from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class FiscalYear(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    year: int
    start_date: date
    end_date: date


class FiscalPeriod(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    fiscal_year_id: int = Field(foreign_key="fiscalyear.id")
    period_number: int
    start_date: date
    end_date: date

    is_open: bool = Field(default=True)
