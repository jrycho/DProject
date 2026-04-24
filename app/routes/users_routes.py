from fastapi import APIRouter, HTTPException, Depends
from app.db_files.crud.users import create_user, get_user_by_email, update_reset_hashes,  hash_password, change_password, email_not_registered
from app.db_files.core.database import get_db
from app.db_files.models.users import UserCreate
from app.utils.forgotten_password import get_reset_token, send_reset_email, hash_token
from datetime import datetime, timezone
from app.db_files.crud.settings_saves import save_user_settings
from fastapi.responses import JSONResponse
from app.security.security import create_access_token
from dotenv import load_dotenv
from app.models.forgotPasswordRequest import ForgotPasswordRequest
from app.models.payload_inputs import ResetPasswordPayload
import os
from app.db_files.crud.user_db_crud import user_shared_keys_init

load_dotenv()
DOMAIN = os.getenv("DOMAIN")

router = APIRouter(prefix="/users", tags=["Users"])
settings_placeholder_values = {
    "optimized_properties": ["calories", "protein", "carbs", "fats"],
    "target_goal": [600.0, 30.0, 60.0, 20.0],
    "excess_weights": [1.0, 1.0, 1.0, 1.0],
    "slack_weights": [1.0, 1.0, 1.0, 1.0],
}
MEAL_TYPES = ["Breakfast", "Snack 1", "Lunch", "Snack 2", "Dinner", "Snack 3"]


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
@router.post("") #! USED
async def signup(user: UserCreate, db=Depends(get_db)):
    email = user.email.lower().strip()
    if not await email_not_registered(db=db, email=email):
        raise HTTPException(status_code=400, detail="Email already exists")
    result = await create_user(db, user)
    uid = result.inserted_id
    for meal_type in MEAL_TYPES:
        await save_user_settings(user_id=str(uid), meal_type=meal_type, settings=settings_placeholder_values)

    
    token = create_access_token(data={"sub": str(uid)})




    """
    response = JSONResponse(content={"message": "User created"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=3600,
    )"""

    
    return {
        "message": "User created",
        "access_token": token,
        "token_type": "bearer"
    }


#NOT YET DONE:
@router.post("/password-reset-requests")
async def forgotten_password(payload: ForgotPasswordRequest, db=Depends(get_db)):
    email = payload.email
    resp = await get_user_by_email(db, email)
    if not resp:
        return {"message": "If email exists, reset link was sent"}
    
    token, token_hash, expires_at = get_reset_token()
    await update_reset_hashes(db =db, email=email, reset_hash=token_hash, expires=expires_at)

    reset_link = f"{DOMAIN}/reset_password?token={token}"
    send_reset_email(email, reset_link)
    

    return {"message": "If email exists, reset link was sent"}





@router.post("/password-resets")
async def reset_password(payload: ResetPasswordPayload, db=Depends(get_db)):
    token_hash = hash_token(payload.token)
    new_pw_hash = hash_password(payload.password)

    success = await change_password(db, token_hash, new_pw_hash)

    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    return {"message": "Password reset successful"}



