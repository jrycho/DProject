from app.db_files.core.database import db
print("settings_saves loaded")
print("Available symbols:", dir())

"""  
ID and dict load
args: user_id: str, settings: dict; will be passed via frontend as JSON
rewrites settings to db
"""
async def save_user_settings(user_id: str, settings: dict):
    return await db.user_settings.update_one(
        {"user_id": user_id},
        {"$set": settings},
        upsert=True
    )
"""  
returns settings dict for user_id
args: user_id: str

"""
async def get_user_settings(user_id: str):
    return await db.user_settings.find_one({"user_id": user_id})