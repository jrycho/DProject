from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from bson import ObjectId
from fastapi import HTTPException, status


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(db, user):
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "is_admin": False,
        "created_at": datetime.now(),
        "share_key": uuid4().hex,
    }
    return await db["users"].insert_one(user_data)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return  pwd_context.verify(plain_password, hashed_password)

async def get_user_by_email(db, email: str):
    user = await db["users"].find_one({"email": email})
    return user

async def get_user_by_token(db, hashed_token: str):
    user = await db["users"].find_one({"reset_hash": hashed_token})
    return user

async def update_reset_hashes(db, email: str, reset_hash: str, expires: datetime):
    await db["users"].update_one({"email": email.lower()}, {"$set": {"reset_hash": reset_hash, "reset_hash_expires": expires}})

async def clear_reset_hashes(db, email: str):
    await db["users"].update_one(
        {"email": email.lower()},
        {"$unset": {
            "reset_hash": "",
            "reset_hash_expires": ""
        }}
    )

async def change_password(db, token_hash: str, new_pw_hash: str):
    user = await db["users"].find_one({"reset_hash": token_hash})

    if not user:
        return False

    expires = user["reset_hash_expires"]

    # make DB datetime UTC-aware if it isn't
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)

    if expires < datetime.now(timezone.utc):
        return False


    await db["users"].update_one(
        {"_id": user["_id"]},
        {
            "$set": {"password": new_pw_hash},
            "$unset": {
                "reset_hash": "",
                "reset_hash_expires": ""
            }
        }
    )

    return True


async def change_username_crud(db, data: dict, new_username: str):
    user_id = ObjectId(data["_id"])
    doc = await db["users"].find_one({"_id": user_id}, {"last_username_change": 1})
    last = doc.get("last_username_change") if doc else None
    print(data)

    now = datetime.now(timezone.utc)
    #return string to datetime

    if isinstance(last, str):
        # handles str to datetime
        last = datetime.fromisoformat(last.replace("Z", "+00:00"))

    #transform to utc 
    if isinstance(last, datetime) and last.tzinfo is None:
        last = last.replace(tzinfo=timezone.utc)

    print(last, now)

    if last is not None and (now - last) < timedelta(hours=24):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Username can only be changed once every 24 hours",)

    result = await db["users"].update_one(
        {"_id": user_id},
        {"$set": {"username": new_username, "last_username_change": now}},
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",)

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already the same",)

    return {"message": "success"}