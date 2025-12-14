# app/core/email_service.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import get_settings

settings = get_settings()


def send_email(to_email: str, subject: str, body: str):
    if not settings.GMAIL_USER or not settings.GMAIL_APP_PASSWORD:
        print("Email disabled: Missing env variables")
        return False

    msg = MIMEMultipart()
    msg["From"] = settings.GMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(settings.GMAIL_USER, settings.GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email failed:", e)
        return False
