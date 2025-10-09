from app.db_files.core.database import db
from fastapi import HTTPException
from app.models.settings import Settings 
print("settings_saves loaded")
print("Available symbols:", dir())

"""  
ID and dict load
args: user_id: str, settings: dict; will be passed via frontend as JSON
rewrites settings to db
"""
async def save_user_settings(user_id: str, settings: dict): #!USED
    return await db.user_settings.update_one(
        {"user_id": user_id},
        {"$set": settings},
        upsert=True
    )
"""  
returns settings dict for user_id
args: user_id: str

"""
async def get_user_settings(user_id: str): #!USED
    data = await db.user_settings.find_one({"user_id": user_id})
    if not data:
        raise HTTPException(status_code=404, detail="Settings not found")
    return data

async def get_settings_obj(user_id: str): #!USED
        db_data = await get_user_settings(user_id)
        # Convert to Settings object
        settings_obj = Settings(**db_data)

        return settings_obj # Return as JSON
