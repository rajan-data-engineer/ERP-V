# app/services/email_service_wrapper.py

from app.core.email_service import send_email
from app.core.config import get_settings

settings = get_settings()


class EmailNotifications:

    @staticmethod
    def notify_admin_new_user(username: str):
        subject = "New ERP-V User Registration"
        body = f"A new user '{username}' has registered and is awaiting approval."
        send_email(settings.GMAIL_USER, subject, body)

    @staticmethod
    def notify_user_approved(email: str):
        subject = "Your ERP-V Account Has Been Approved"
        body = "Your account has now been activated. You may log in and start using ERP-V."
        send_email(email, subject, body)

    @staticmethod
    def notify_admin_failed_login(username: str):
        subject = "Failed Login Attempt"
        body = f"A failed login attempt was detected for username '{username}'."
        send_email(settings.GMAIL_USER, subject, body)

    @staticmethod
    def notify_admin_journal_posted(journal_id: int):
        subject = "Journal Posted"
        body = f"Journal Entry {journal_id} has been posted successfully."
        send_email(settings.GMAIL_USER, subject, body)
