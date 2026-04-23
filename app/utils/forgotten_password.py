import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from email.utils import formataddr
import os
from dotenv import load_dotenv
import smtplib
import ssl


load_dotenv()


RESET_TOKEN_MINUTES = 30
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.cesky-hosting.cz")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_SECURITY = os.getenv("SMTP_SECURITY", "tls").lower()
SMTP_USER = os.getenv("SMTP_USER", "noreply@jrycho.cz")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USER)
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Jrycho")


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
    if not SMTP_PASS:
        raise RuntimeError("SMTP_PASS environment variable is required to send reset emails")

    text = f"""Reset your password

We received a request to reset your password.

Reset link: {reset_link}

This link expires in {RESET_TOKEN_MINUTES} minutes.

If you did not request this, you can safely ignore this email.
"""

    html = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.5;">
        <h2>Reset your password</h2>
        <p>We received a request to reset your password.</p>
        <p>
            <a href="{reset_link}" style="display:inline-block;padding:10px 16px;text-decoration:none;border-radius:6px;">
                Reset Password
            </a>
        </p>
        <p>This link expires in {RESET_TOKEN_MINUTES} minutes.</p>
        <p>If you did not request this, you can safely ignore this email.</p>
    </div>
    """

    message = EmailMessage()
    message["From"] = formataddr((SMTP_FROM_NAME, SMTP_FROM_EMAIL))
    message["To"] = to_email
    message["Subject"] = "Reset your password"
    message.set_content(text)
    message.add_alternative(html, subtype="html")

    if SMTP_SECURITY == "ssl":
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ssl.create_default_context()) as smtp:
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(message)
    else:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            if SMTP_SECURITY == "tls":
                smtp.starttls(context=ssl.create_default_context())
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(message)
