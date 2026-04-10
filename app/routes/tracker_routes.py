from fastapi import APIRouter, HTTPException, Depends
from app.db_files.crud.user_db_crud import search_crud, create_user_ingredients, get_user_ingredients, get_user_key as get_user_key_crud, add_user_shared_keys as add_user_shared_keys_crud, get_user_shared_keys as get_user_shared_keys_crud
from app.db_files.crud.meal_logs_crud import ingredient_doc_to_button_json
from app.security.security import get_current_user_id
from app.db_files.crud.tracker_crud import save_new_user_goal, get_user_goals, find_meal_logs_of_user_and_date, get_macros_from_meal_log, sum_macros_from_meals
from app.models.payload_inputs import DatePayload, DatedMacroGoalsPayload, EstimateUserMacrosPayload


router = APIRouter(prefix="/Tracker", tags=["Tracker"])

@router.post("/estimate_user_macros")
async def estimate_user_macros(payload: EstimateUserMacrosPayload, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="User not found")
    
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


@router.post("/set_user_goals")
async def set_user_goals(custom_goal: DatedMacroGoalsPayload, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="User not found")
    resp = await save_new_user_goal(
        user_goal=custom_goal.target_macros,
        user_id=user_id,
        goal_date=custom_goal.goal_date,
    )
    if resp.modified_count==0 and resp.upserted_id is None:
        raise HTTPException(status_code=400, detail="No changes made")
    return {"detail": "Successfully updated goals"}

@router.post("/fetch_tracker_data")
async def fetch_tracker_data(payload: DatePayload, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="User not found")
    resp = await get_user_goals(user_id=user_id, requested_date=payload.date)
    if resp is None:
        raise HTTPException(status_code=400, detail="No data found")
    return resp

@router.post("/calculate_daily_macros")
async def calculate_daily_macros(payload: DatePayload = Depends(), user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    # find meal ids of the day
    list_of_meal_logs = await find_meal_logs_of_user_and_date(user_id=user_id, date=payload.date)
    print(f"list_of_meal_logs: {list_of_meal_logs}")
    if list_of_meal_logs is None:
        raise HTTPException(status_code=400, detail="No data found")
    #find results of each meal
    ids_list = []
    print(f"ids_list: {ids_list}")
    for item in list_of_meal_logs:
        ids_list.append(item.get("meal_id"))

        
        
    #sum all macros
    print("Trying to sum macros")
    resp = await sum_macros_from_meals(ids_list=ids_list)
    if resp is None:
        raise HTTPException(status_code=400, detail="No data found")
    return resp
