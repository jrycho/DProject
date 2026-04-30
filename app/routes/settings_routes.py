from fastapi import APIRouter, HTTPException, Depends
from app.models.settings import Settings
from app.db_files.crud.settings_saves import save_user_settings, get_user_settings
from app.security.security import get_current_user_id
from app.models.payload_inputs import MealTypePayload, SettingsPayload

router = APIRouter(prefix="/settings", tags=["User Settings"])

"""  
Create or update meal settings.
This route saves optimizer settings for one meal type for the current user.
Args:
    - input (SettingsPayload): Meal type and settings values.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Success message and user ID.
"""
@router.post("") #! USED, worth 
async def create_settings(input: SettingsPayload, user_id: str = Depends(get_current_user_id)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    settings_obj = Settings(
        excess_weights=input.excess_weights,
        slack_weights=input.slack_weights,
        target_goal=input.target_goal,
        optimized_properties=input.optimized_properties,
    )
    meal_type = input.meal_type.strip()

    try:
        await save_user_settings(user_id=user_id,meal_type=meal_type, settings= settings_obj.model_dump())
        return {"message": "Settings saved", "user_id": user_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""  
Get meal settings.
This route fetches saved optimizer settings for one meal type for the current user.
Args:
    - payload (MealTypePayload): Meal type to fetch.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Saved settings data.
"""
@router.post("/items") #! USED
async def get_settings(payload: MealTypePayload, user_id: str = Depends(get_current_user_id)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    meal_type = payload.meal_type
    db_data = await get_user_settings(user_id=user_id,meal_type=meal_type)
    if not db_data:
        raise HTTPException(status_code=404, detail="Settings not found")

    settings_obj = Settings(**db_data)
    return settings_obj.model_dump()
 
