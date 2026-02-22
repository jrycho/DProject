from fastapi import APIRouter, HTTPException, Depends
from app.db_files.crud.users import create_user, get_user_by_email, update_reset_hashes, clear_reset_hashes, get_user_by_token, hash_password, change_password
from app.db_files.core.database import get_db
from app.db_files.models.users import UserCreate
from app.utils.forgotten_password import get_reset_token, send_reset_email, hash_token
from datetime import datetime, timezone


router = APIRouter(prefix="/Signup", tags=["Signup"])

"""  
signup router
Args: 
    user: UserCreate
    db: Session
Returns: 
    confirmation message and signs to db
Raises: 
    HTTPException: 400 if user already exists
"""
@router.post("/signup") #! USED
async def signup(user: UserCreate, db=Depends(get_db)):
    if await db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    result = await create_user(db, user)
    uid = result.inserted_id
    await db.user_settings.update_one(
        {"user_id": uid},
        {"$setOnInsert": {
            "user_id": uid,
            "schema_version": 1,
            "optimized_properties": ["kcal","protein","carbs","fat"],
            "target_goal": {"kcal": 600.0, "protein": 30.0, "carbs": 60.0, "fat": 20.0},
            "excess_weights": {"kcal":1.0,"protein":1.0,"carbs":1.0,"fat":1.0},
            "slack_weights":  {"kcal":1.0,"protein":1.0,"carbs":1.0,"fat":1.0},
        }},
        upsert=True,
    )
    await db.user_settings.create_index("user_id", unique=True)

    
    return {"message": "User created", "user_id": str(result.inserted_id)}


#NOT YET DONE:
@router.post("/forgotten_password")
async def forgotten_password(email: str, db=Depends(get_db)):
    resp = await get_user_by_email(db, email)
    if not resp:
        return {"message": "If email exists, reset link was sent"}
    
    token, token_hash, expires_at = get_reset_token()
    await update_reset_hashes(db = Depends(get_db), email=email, token_hash=token_hash, expires_at=expires_at)

    reset_link = f"http://localhost:3000/reset-password?token={token}"
    send_reset_email(email, reset_link)
    

    return {"message": "Password reset link sent to your email"}





@router.post("/reset_password")
async def reset_password(token: str, password: str, db=Depends(get_db)):
    token_hash = hash_token(token)
    new_pw_hash = hash_password(password)

    success = await change_password(db, token_hash, new_pw_hash)

    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    return {"message": "Password reset successful"}



