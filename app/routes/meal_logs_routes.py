from fastapi import APIRouter, HTTPException, Depends
from app.db_files.crud.meal_logs_crud import create_meal_log, add_ingredient_to_log, delete_ingredient_from_meal_log, get_meal_by_date, return_ingredients_button, update_ingredient_amount_settings_crud
from app.db_files.crud.ingredient_crud import get_or_fetch_ingredient_dict_sync, doc_to_ingredient_entry
from uuid import uuid4
from app.security.security import get_current_user_id
from datetime import datetime
import logging
from app.models.payload_inputs import DatePayload, MealLogPayload, MealLogWithIdPayload, SetAndPieceWeightsPayload



log = logging.getLogger(__name__)

router = APIRouter(prefix="/meal-logs", tags=["Meal Logs"])


"""  
Log a meal with a provided meal ID.
This route is useful for tests or clients that need a known meal_id.
Args:
    - payload (MealLogWithIdPayload): Meal type, date, and meal_id.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Message, meal_id, user_id, and created log_id.
"""
@router.post("/custom-id") #!USED testing
async def log_meal_with_id(payload: MealLogWithIdPayload = Depends(), user_id: str = Depends(get_current_user_id)): 
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    try:

        date = str(payload.date)
        meal_id = str(payload.meal_id)
        user_id = str(user_id)
        meal_type = str(payload.meal_type)
    
        log_id = await create_meal_log(
            meal_id=meal_id,
            user_id=user_id,
            type_of_meal=meal_type,
            date=date,
            )
        return {"message": "Meal logged", "meal_id": meal_id, "user_id": user_id, "log_id": log_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
"""  
Log a meal and create its meal ID.
This route creates a new meal log for the current user.
Args:
    - payload (MealLogPayload): Meal type and date.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Message, created log_id, meal_id, and user_id.
"""
@router.post("") #!USED
async def log_meal(payload: MealLogPayload = Depends(), user_id: str = Depends(get_current_user_id)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    try:
        meal_id = str(uuid4())
        user_id = str(user_id)
        meal_type = str(payload.meal_type)

        log_id = await create_meal_log(
            meal_id=meal_id,
            user_id=user_id,
            type_of_meal=meal_type,
            date=payload.date,
            )
        return {
            "message": "Meal logged",
            "log_id": log_id,
            "meal_id": meal_id,
            "user_id": user_id
        }
    except HTTPException:
        raise
    except Exception as e:
        log.exception("log_meal failed")
        raise HTTPException(status_code=500, detail=str(e))

"""  
Remove ingredient by barcode.
This route removes one ingredient from the current user's meal log.
Args:
    - meal_id (str): Target meal ID.
    - barcode (str): Ingredient barcode.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Success message.
"""
@router.delete("/{meal_id}/ingredients") #!USED
async def remove_ingredient_by_barcode(meal_id: str, barcode: str, user_id: str = Depends(get_current_user_id)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    res = await delete_ingredient_from_meal_log(meal_id, barcode, user_id)
    return res


"""  
Fetch meals for the current user by date.
This route validates date format before querying meal logs.
Args:
    - payload (DatePayload): Date to search for.
    - current_user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - list: Meal logs for that date.
"""
@router.get("/by-date") #!USED
async def fetch_meal_by_date(payload: DatePayload = Depends(), current_user_id: str = Depends(get_current_user_id)):
    if not current_user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    try:
        datetime.fromisoformat(payload.date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    res = await get_meal_by_date(current_user_id, payload.date)
    return res


"""  
Add an ingredient to a meal log.
This route fetches ingredient data by barcode and saves it to the meal.
Args:
    - barcode (str): Ingredient barcode.
    - meal_id (str): Target meal ID.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Success message.
"""
@router.post("/{meal_id}/ingredients/{barcode}") #!USED
async def add_ingredient(barcode: str, meal_id: str, user_id: str = Depends(get_current_user_id)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    doc = await get_or_fetch_ingredient_dict_sync(barcode)
    entry = await doc_to_ingredient_entry(doc, 1)
    res = await add_ingredient_to_log(meal_id, user_id, entry)
    return res

"""  
Return ingredients for meal ingredient buttons.
This route loads saved meal ingredients and formats them for frontend buttons.
Args:
    - meal_id (str): Target meal ID.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - list: Ingredient button data.
"""
@router.get("/{meal_id}/ingredients")
async def return_ingredients_for_buttons(meal_id: str, user_id: str = Depends(get_current_user_id)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    data = await return_ingredients_button(meal_id, user_id)
    return data


"""  
Update ingredient amount settings.
This route saves piece weight, set amount, and min/max amount for one ingredient.
Args:
    - payload (SetAndPieceWeightsPayload): Ingredient amount settings.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Update result.
"""
@router.post("/ingredient-amount-settings")
async def update_ingredient_amount_settings(payload: SetAndPieceWeightsPayload = Depends(), user_id: str = Depends(get_current_user_id)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    data = await update_ingredient_amount_settings_crud(
        barcode=payload.barcode,
        meal_id=payload.meal_id,
        user_id=user_id,
        set_amount=payload.set_amount,
        piece_weight=payload.piece_weight,
        min_amount=payload.min_amount,
        max_amount=payload.max_amount,
    )
    return data
