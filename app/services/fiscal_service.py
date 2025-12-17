from sqlmodel import Session, select
from datetime import date, datetime

from app.models.fiscal import FiscalPeriod


class FiscalService:

    # ---------------------------------
    # CREATE FISCAL PERIOD
    # ---------------------------------
    @staticmethod
    def create_period(
        fiscal_year: int,
        period_number: int,
        start_date: str,
        end_date: str,
        session: Session
    ):
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)

        # Check overlap
        existing = session.exec(
            select(FiscalPeriod)
            .where(FiscalPeriod.start_date <= end)
            .where(FiscalPeriod.end_date >= start)
        ).first()

        if existing:
            raise ValueError("Period overlaps with an existing fiscal period.")

        period = FiscalPeriod(
            fiscal_year=fiscal_year,
            period_number=period_number,
            start_date=start,
            end_date=end,
            is_closed=False
        )

        session.add(period)
        session.commit()
        session.refresh(period)

        return period

    # ---------------------------------
    # LIST PERIODS
    # ---------------------------------
    @staticmethod
    def list_periods(session: Session):
        return session.exec(
            select(FiscalPeriod).order_by(
                FiscalPeriod.fiscal_year,
                FiscalPeriod.period_number
            )
        ).all()

    # ---------------------------------
    # CLOSE PERIOD
    # ---------------------------------
    @staticmethod
    def close_period(period_id: int, session: Session):
        period = session.get(FiscalPeriod, period_id)
        if not period:
            raise ValueError("Fiscal period not found.")
        period.is_closed = True
        session.commit()
        return {"message": "Fiscal period closed"}

    # ---------------------------------
    # OPEN PERIOD
    # ---------------------------------
    @staticmethod
    def open_period(period_id: int, session: Session):
        period = session.get(FiscalPeriod, period_id)
        if not period:
            raise ValueError("Fiscal period not found.")
        period.is_closed = False
        session.commit()
        return {"message": "Fiscal period opened"}

    # ---------------------------------
    # GET PERIOD FOR A GIVEN DATE
    # ---------------------------------
    @staticmethod
    def get_period_for_date(eff_date: datetime, session: Session):
        return session.exec(
            select(FiscalPeriod)
            .where(FiscalPeriod.start_date <= eff_date.date())
            .where(FiscalPeriod.end_date >= eff_date.date())
        ).first()

    # ---------------------------------
    # VALIDATE BEFORE POSTING
    # ---------------------------------
    @staticmethod
    def validate_posting_date(eff_date: datetime, session: Session):
        period = FiscalService.get_period_for_date(eff_date, session)

        if not period:
            raise ValueError("No fiscal period is defined for this date.")

        if period.is_closed:
            raise ValueError("Posting date falls into a CLOSED fiscal period.")

        return True
