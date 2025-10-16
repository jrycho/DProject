from passlib.context import CryptContext
from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(db, user):
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "is_admin": False,
        "created_at": datetime.now()
    }
    return await db["users"].insert_one(user_data)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return  pwd_context.verify(plain_password, hashed_password)

