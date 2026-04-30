from app.db_files.core.database import db
from fastapi import HTTPException
from app.models.settings import Settings
from datetime import datetime, timezone

settings_collection = db.user_settings

"""  
Save user settings for one meal type.
Args:
    - user_id (str): Owner of the settings.
    - meal_type (str): Meal type key.
    - settings (dict): Settings data to save.
Returns:
    - UpdateResult: MongoDB update result.
Usage:
    - app/routes/settings_routes.py: create_settings
    - app/routes/users_routes.py: create_user
Workflow:
    - Match user settings document by user_id.
    - Store settings under meals.<meal_type>.
    - Update updated_at timestamp.
    - Create user settings document if it does not exist.
    - Return MongoDB update result.
"""
async def save_user_settings(user_id: str, meal_type:str, settings: dict): #!USED
    res = await settings_collection.update_one(
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
    return res

"""  
Get saved settings for one meal type.
Args:
    - user_id (str): Owner of the settings.
    - meal_type (str): Meal type key.
Returns:
    - dict: Saved settings for the meal type.
Usage:
    - app/routes/settings_routes.py: get_settings
    - Internal helper for get_settings_obj.
Workflow:
    - Find user settings document by user_id.
    - Read settings under meals.<meal_type>.
    - Raise 404 if settings are missing.
    - Return settings dict.
"""
async def get_user_settings(user_id: str, meal_type:str): #!USED
    data = await settings_collection.find_one(
        {"user_id": user_id
        },
        projection={"_id": 0, "user_id": 0}
    ) or {}
    resp = data.get("meals", {}).get(meal_type)
    if not resp:
        raise HTTPException(status_code=404, detail="Data not found")
    return resp

    
"""  
Get saved settings as a Settings object.
Args:
    - user_id (str): Owner of the settings.
    - meal_type (str): Meal type key.
Returns:
    - Settings: Validated settings object.
Usage:
    - app/routes/optimization_routes.py: optimize_meal
    - Uses get_user_settings internally.
Workflow:
    - Fetch settings dict for user_id and meal_type.
    - Raise 404 if settings are missing.
    - Convert settings dict into Settings model.
    - Return Settings object for optimizer use.
"""
async def get_settings_obj(user_id: str, meal_type:str): #!USED
        db_data = await get_user_settings(user_id=user_id, meal_type=meal_type)
        if not db_data:
            raise HTTPException(status_code=404, detail="Data not found")
        settings_obj = Settings(**db_data)

        return settings_obj
 
