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
@router.post("/signup")
async def signup(user: UserCreate, db=Depends(get_db)):
    if await db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    result = await create_user(db, user)
    return {"message": "User created", "user_id": str(result.inserted_id)}