import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage 
import os
from dotenv import load_dotenv
import smtplib
import resend


load_dotenv()
resend_api_key = os.getenv("RESEND_API_KEY")





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

    return resend.Emails.send(
        {
            "from": "Test <onboarding@resend.dev>",
            "to": [to_email],
            "subject": "Reset your password",
            "html": html,
        }
    )
