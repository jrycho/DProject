from app.db_files.core.database import db
from fastapi import HTTPException
from app.models.settings import Settings 
from pymongo import errors as mongo_errors
print("settings_saves loaded")
print("Available symbols:", dir())

default_settings = {  "excess_weights": [10,10,8,5],
  "optimized_properties": ["calories","protein","carbs","fats"],
  "slack_weights": [0,0,0,10],
  "target_goal": [300,20,40,12]}
"""  
ID and dict load
args: user_id: str, settings: dict; will be passed via frontend as JSON
rewrites settings to db
"""
async def save_user_settings(user_id: str, settings: dict): #!USED
    return await db.user_settings.update_one(
        {"user_id": user_id},
        {"$set":  settings, 
         "$setOnInsert": {"user_id": user_id}},
        upsert=True
    )
"""  
returns settings dict for user_id
args: user_id: str

"""
async def get_user_settings(user_id: str): #!USED
    try:
        data = await db.user_settings.find_one({"user_id": user_id},
                                                projection={"_id": 0, "user_id": 0})
        if data is None:
            await save_user_settings(user_id, default_settings)
            data = await db.user_settings.find_one({"user_id": user_id},
                                                projection={"_id": 0, "user_id": 0})
        return data
    
    except (mongo_errors.ServerSelectionTimeoutError,
            mongo_errors.NetworkTimeout,
            mongo_errors.AutoReconnect) as e:
         raise HTTPException(status_code=503, detail="Database unavailable") from e
    
    except mongo_errors.PyMongoError as e:
        # anything else that's a DB error (bad query, auth, etc.)
        raise HTTPException(status_code=500, detail="Database error") from e

    

async def get_settings_obj(user_id: str): #!USED
        db_data = await get_user_settings(user_id)
        if not db_data:
            raise HTTPException(status_code=404, detail="Data not found")
        # Convert to Settings object
        settings_obj = Settings(**db_data)

        return settings_obj # Return as JSON
