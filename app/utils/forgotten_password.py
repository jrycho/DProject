import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage 
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

MAILTRAP_HOST = "sandbox.smtp.mailtrap.io"
MAILTRAP_PORT = 587
MAILTRAP_USER = "ca979ca8ebdfce"
MAILTRAP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = "noreply@jrnoreply.com"



RESET_TOKEN_MINUTES = 30


def make_reset_token():
    return secrets.token_urlsafe(48)


def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()


def get_reset_token():
    token = make_reset_token()
    token_h = hash_token(token)

    expires = datetime.now(timezone.utc) + timedelta(
        minutes=RESET_TOKEN_MINUTES
    )

    return token, token_h, expires


def send_reset_email(to_email, reset_link):
    msg = EmailMessage()
    msg["Subject"] = "Reset your password"
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    msg.set_content(
            f"""
    You requested a password reset.

    Reset link (valid 30 minutes):
    {reset_link}

    If you didn’t request this, ignore this email.
    """
        )

    with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as server:
        server.starttls()
        server.login(MAILTRAP_USER, MAILTRAP_PASS)
        server.send_message(msg)