from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from bson import ObjectId
from fastapi import HTTPException
from pymongo.errors import PyMongoError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""  
Hash a plain password.
Args:
    - password (str): Plain password.
Returns:
    - str: Hashed password.
Usage:
    - app/routes/users_routes.py: signup
    - app/routes/users_routes.py: reset_password
    - app/tests/auth_tests.py
Workflow:
    - Hash password using passlib context.
    - Return password hash.
"""
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

"""  
Create a user document.
Args:
    - db: Database dependency.
    - user: UserCreate payload.
Returns:
    - InsertOneResult: MongoDB insert result.
Usage:
    - app/routes/users_routes.py: signup
Workflow:
    - Build user document from signup payload.
    - Hash user password.
    - Add default admin flag, created_at, share_key, and shared_keys.
    - Insert document into users collection.
    - Return insert result.
"""
async def create_user(db, user):
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "is_admin": False,
        "created_at": datetime.now(),
        "share_key": uuid4().hex,
        "shared_keys": []
    }
    return await db["users"].insert_one(user_data)

"""  
Verify a plain password against a hash.
Args:
    - plain_password (str): Plain password from login.
    - hashed_password (str): Stored password hash.
Returns:
    - bool: True when password matches.
Usage:
    - app/routes/login_routes.py: login
Workflow:
    - Verify password using passlib context.
    - Return verification result.
"""
async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return  pwd_context.verify(plain_password, hashed_password)

"""  
Get user by email.
Args:
    - db: Database dependency.
    - email (str): User email.
Returns:
    - dict: User document.
Usage:
    - app/routes/login_routes.py: login
    - app/routes/users_routes.py: forgotten_password
Workflow:
    - Query users collection by email.
    - Convert MongoDB errors to runtime error.
    - Raise 404 if no user exists.
    - Return user document.
"""
async def get_user_by_email(db, email: str):
    try:
        user = await db["users"].find_one({"email": email})
    except PyMongoError as e:
        raise RuntimeError(f"Error retrieving user by email: {e}")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

"""  
Get user by password reset token hash.
Args:
    - db: Database dependency.
    - hashed_token (str): Hashed reset token.
Returns:
    - dict | None: User document if token hash exists.
Usage:
    - Currently no active call site found in app/.
Workflow:
    - Query users collection by reset_hash.
    - Return user document or None.
"""
async def get_user_by_token(db, hashed_token: str):
    user = await db["users"].find_one({"reset_hash": hashed_token})
    return user

"""  
Save password reset hash and expiration.
Args:
    - db: Database dependency.
    - email (str): User email.
    - reset_hash (str): Hashed reset token.
    - expires (datetime): Expiration datetime.
Returns:
    - None
Usage:
    - app/routes/users_routes.py: forgotten_password
Workflow:
    - Match user by lowercase email.
    - Save reset_hash and reset_hash_expires.
"""
async def update_reset_hashes(db, email: str, reset_hash: str, expires: datetime):
    await db["users"].update_one({"email": email.lower()}, {"$set": {"reset_hash": reset_hash, "reset_hash_expires": expires}})

"""  
Clear password reset hash fields.
Args:
    - db: Database dependency.
    - email (str): User email.
Returns:
    - None
Usage:
    - Currently no active call site found in app/.
Workflow:
    - Match user by lowercase email.
    - Remove reset_hash and reset_hash_expires fields.
"""
async def clear_reset_hashes(db, email: str):
    await db["users"].update_one(
        {"email": email.lower()},
        {"$unset": {
            "reset_hash": "",
            "reset_hash_expires": ""
        }}
    )

"""  
Change password using reset token hash.
Args:
    - db: Database dependency.
    - token_hash (str): Hashed reset token.
    - new_pw_hash (str): New password hash.
Returns:
    - bool: True when password was changed.
Usage:
    - app/routes/users_routes.py: reset_password
Workflow:
    - Find user by reset token hash.
    - Return False if token is missing.
    - Normalize expiration datetime to UTC.
    - Return False if token is expired.
    - Save new password hash.
    - Clear reset token fields.
    - Return True.
"""
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


"""  
Change user's username.
Args:
    - db: Database dependency.
    - data (dict): Current user data.
    - new_username (str): New username.
Returns:
    - dict: Success message.
Usage:
    - app/routes/login_routes.py: change_username
Workflow:
    - Convert current user _id to ObjectId.
    - Load last username change timestamp.
    - Normalize timestamp to timezone-aware UTC.
    - Enforce 24 hour username change limit.
    - Update username and last_username_change.
    - Raise 404 if user is missing.
    - Raise 409 if username is unchanged.
    - Return success message.
"""
async def change_username_crud(db, data: dict, new_username: str):
    user_id = ObjectId(data["_id"])
    doc = await db["users"].find_one({"_id": user_id}, {"last_username_change": 1})
    last = doc.get("last_username_change") if doc else None

    now = datetime.now(timezone.utc)
    #return string to datetime

    if isinstance(last, str):
        # handles str to datetime
        last = datetime.fromisoformat(last.replace("Z", "+00:00"))

    #transform to utc 
    if isinstance(last, datetime) and last.tzinfo is None:
        last = last.replace(tzinfo=timezone.utc)

    if last is not None and (now - last) < timedelta(hours=24):
        raise HTTPException(
            status_code=429,
            detail="Username can only be changed once every 24 hours",)

    result = await db["users"].update_one(
        {"_id": user_id},
        {"$set": {"username": new_username, "last_username_change": now}},
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found",)

    if result.modified_count == 0:
        raise HTTPException(
            status_code=409,
            detail="Username is already the same",)

    return {"message": "success"}


"""  
Delete a user by ID.
Args:
    - db: Database dependency.
    - user_id (str): User ID.
Returns:
    - bool: True when user was deleted.
Usage:
    - Currently no active call site found in app/.
Workflow:
    - Delete user document by _id.
    - Raise 404 if no user was deleted.
    - Return True.
"""
async def clear_user(db, user_id:str):
    resp = await db["users"].delete_one({"_id": (user_id)})
    if resp.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found",)
    return True


"""  
Get user by ObjectId.
Args:
    - collection: Users collection.
    - user_id (ObjectId): User ObjectId.
Returns:
    - dict | None: User document.
Usage:
    - app/security/security.py: get_current_user
Workflow:
    - Query collection by _id.
    - Return user document.
    - Convert MongoDB errors to HTTP 500.
"""
async def get_user_by_ObjectID(collection, user_id: ObjectId):
    try:
        user = await collection.find_one({"_id": user_id})
        return user
    except PyMongoError as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",)

"""  
Check if email is not registered.
Args:
    - db: Database dependency.
    - email (str): Email to check.
Returns:
    - bool: True when email is available.
Usage:
    - app/routes/users_routes.py: signup
Workflow:
    - Query users collection by email.
    - Return False when user exists.
    - Return True when email is available.
    - Convert MongoDB errors to HTTP 500.
"""
async def email_not_registered(db, email: str):
    try:
        user = await db["users"].find_one({"email": email})
        if user:
            return False
        return True
    except PyMongoError as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",)
