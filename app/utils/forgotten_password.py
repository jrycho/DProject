import secrets
import hashlib
from datetime import datetime, timedelta, timezone

RESET_TOKEN_MINUTES = 30

def make_reset_token() -> str:
    return secrets.token_urlsafe(48)

def hash_token(token: str) -> str:
    # stable + fast hash is fine here (token is high entropy)
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def now_utc() -> datetime:
    return datetime.now(timezone.utc)