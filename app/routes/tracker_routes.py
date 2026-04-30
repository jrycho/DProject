from fastapi import APIRouter, HTTPException, Depends
from app.security.security import get_current_user_id
from app.db_files.crud.tracker_crud import save_new_user_goal, get_user_goals, find_meal_logs_of_user_and_date, sum_macros_from_meals
from app.models.payload_inputs import DatePayload, DatedMacroGoalsPayload, EstimateUserMacrosPayload


router = APIRouter(prefix="/tracker", tags=["Tracker"])

"""  
Estimate and save user macro goals.
This route calculates daily macro targets from user profile inputs and saves them.
Args:
    - payload (EstimateUserMacrosPayload): Body data for macro estimation.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - str: Success message.
"""
@router.post("/macro-estimates")
async def estimate_user_macros(payload: EstimateUserMacrosPayload, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    if payload.sex == "male":
        bmr = 10 * payload.weight + 6.25 * payload.height - 5 * payload.age + 5
    else:
        bmr = 10 * payload.weight + 6.25 * payload.height - 5 * payload.age - 161
    
    activity_factors = {
            "sedentary": 1.2,
            "lightly_active": 1.375,
            "moderately_active": 1.55,
            "very_active": 1.725,
            "athlete": 1.9,
        }
    factor = activity_factors[payload.activity_level]

    tdee = bmr * factor
    
    goal_adjust = {
        "weight_loss": -350,
        "maintain": 0,
        "weight_gain": 350,
    }[payload.goal]

    calories = tdee + goal_adjust

    weight = payload.weight
    protein_g = 1.8 * weight
    fat_g = 0.9 * weight
    carbs_g = (calories - (protein_g * 4 + fat_g * 9)) / 4
    carbs_g = max(0.0, carbs_g)  # prevent negative carbs
    
    macros = {
        "calories": round(calories),
        "protein": round(protein_g, 1),
        "fat": round(fat_g, 1),
        "carbs": round(carbs_g, 1),
        "sat_fat": round(0.07 * calories / 9, 1),
        "fiber": round(14 * (calories / 1000), 1),
        "sodium": 2300,
        "salt": 5.8,
        "cholesterol": 300,
    }
    resp = await save_new_user_goal(
        user_goal=macros,
        user_id=user_id,
        goal_date=payload.goal_date,
    )
    if resp.modified_count==0 and resp.upserted_id is None:
        raise HTTPException(status_code=400, detail="No changes made")
    return ("Successfully updated goals")


"""  
Save custom user macro goals.
This route stores manually provided macro goals for a date.
Args:
    - custom_goal (DatedMacroGoalsPayload): Custom macro goals and date.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Success message.
"""
@router.post("/goals")
async def set_user_goals(custom_goal: DatedMacroGoalsPayload, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    resp = await save_new_user_goal(
        user_goal=custom_goal.target_macros,
        user_id=user_id,
        goal_date=custom_goal.goal_date,
    )
    if resp.modified_count==0 and resp.upserted_id is None:
        raise HTTPException(status_code=400, detail="No changes made")
    return {"detail": "Successfully updated goals"}

"""  
Fetch tracker goals for a date.
This route resolves the current user's macro goals for the requested date.
Args:
    - payload (DatePayload): Requested date.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Resolved goal data.
"""
@router.post("/goals/items")
async def fetch_tracker_data(payload: DatePayload, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    resp = await get_user_goals(user_id=user_id, requested_date=payload.date)
    if resp is None:
        raise HTTPException(status_code=400, detail="No data found")
    return resp

"""  
Calculate daily macros from optimized meals.
This route finds meal logs for a date and sums their saved optimized macros.
Args:
    - payload (DatePayload): Requested date.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Summed macro totals.
"""
@router.post("/daily-macros")
async def calculate_daily_macros(payload: DatePayload = Depends(), user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    # find meal logs of the requested day
    list_of_meal_logs = await find_meal_logs_of_user_and_date(user_id=user_id, date=payload.date)
    if list_of_meal_logs is None:
        raise HTTPException(status_code=400, detail="No data found")

    # collect meal ids from the logs
    ids_list = []
    for item in list_of_meal_logs:
        ids_list.append(item.get("meal_id"))
        
    # sum saved optimized macros for those meal ids
    resp = await sum_macros_from_meals(ids_list=ids_list)
    if resp is None:
        raise HTTPException(status_code=400, detail="No data found")
    return resp
