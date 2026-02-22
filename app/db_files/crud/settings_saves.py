from app.db_files.core.database import db
from fastapi import HTTPException
from app.models.settings import Settings , SettingsInput
from pymongo import errors as mongo_errors
from datetime import datetime, timezone
print("settings_saves loaded")
print("Available symbols:", dir())

settings_collection = db.user_settings

default_settings = SettingsInput(excess_weights=[10,10,8,5],
  optimized_properties=["calories","protein","carbs","fats"],
  slack_weights= [0,0,0,10],
  target_goal=[300,20,40,12])
"""  
ID and dict load
args: user_id: str, settings: dict; will be passed via frontend as JSON
rewrites settings to db
"""
async def save_user_settings(user_id: str, meal_type:str, settings: dict): #!USED
    return await settings_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                f"meals.{meal_type}": settings,
                "updated_at": datetime.now(timezone.utc),
            },
            "$setOnInsert": {"user_id": user_id},
        },
        upsert=True,
    )
"""  
returns settings dict for user_id
args: user_id: str

"""
async def get_user_settings(user_id: str, meal_type:str): #!USED
    data = await settings_collection.find_one(
        {"user_id": user_id},
        projection={"_id": 0, "user_id": 0}
    ) or {}

    meals = data.get("meals") or {}
    resp = meals.get(meal_type)

    if resp is None:
        # create default settings for this meal
        await save_user_settings(
            user_id=user_id,
            meal_type=meal_type,
            settings=default_settings,  # must be a dict
        )
        return default_settings

    return resp

    

async def get_settings_obj(user_id: str): #!USED
        db_data = await get_user_settings(user_id)
        if not db_data:
            raise HTTPException(status_code=404, detail="Data not found")
        # Convert to Settings object
        settings_obj = Settings(**db_data)

        return settings_obj # Return as JSON
 