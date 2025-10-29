from fastapi import APIRouter, HTTPException, Depends
from app.models.settings import SettingsInput
from app.models.settings import Settings  #
from app.db_files.crud.settings_saves import save_user_settings, get_user_settings
import app.state.state as state  # global memory state
from app.security.security import get_current_user_id
from app.utils.settingsPayload import SettingsPayload

router = APIRouter(prefix="/settings", tags=["User Settings"])

"""  
takes SettingsInput in JSON format (via frontend in the future)
args: user_id: str

create settings object
saves it to state
saves it to MongoDB
returns message and user_id
"""
@router.post("/save_settings") #! USED, worth 
async def create_settings(input: SettingsPayload, user_id: str = Depends(get_current_user_id)):
    print(input.excess_weights)
    settings_obj = Settings(
        excess_weights=input.excess_weights,
        slack_weights=input.slack_weights,
        target_goal=input.target_goal,
        optimized_properties=input.optimized_properties,
    )
    print(settings_obj)
    # Save to MongoDB
    try:
        await save_user_settings(user_id, settings_obj.model_dump())
        return {"message": "Settings saved", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""  
takes user_id as a path parameter fetches from DB
args: user_id: str
if not in DB HTTPException 404
returns Settings object
"""
@router.get("/get_settings") #! USED
async def get_settings(user_id: str = Depends(get_current_user_id)):
    try:
        # Get from MongoDB
        db_data = await get_user_settings(user_id)
        if not db_data:
            raise HTTPException(status_code=404, detail="Settings not found")

        # Convert to Settings object
        settings_obj = Settings(**db_data)
        return settings_obj.model_dump()  # Return as JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))