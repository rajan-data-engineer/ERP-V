from sqlmodel import Session
from app.core.posting_engine import PostingEngine

class AccountingService:

    @staticmethod
    def post_journal(session: Session, journal_id: int, user_id: int):
        return PostingEngine.post_journal(session, journal_id, user_id)
