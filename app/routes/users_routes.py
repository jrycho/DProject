from fastapi import APIRouter, HTTPException, Depends
from app.db_files.crud.users import create_user
from app.db_files.core.database import get_db
from app.db_files.models.users import UserCreate


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