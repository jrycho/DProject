from fastapi import APIRouter, HTTPException, Depends

from app.optimizers.gwo_optimizer import gwo_optimizer
from app.optimizers.linprog_optimizer import linprog_optimizer
from app.db_files.crud.settings_saves import get_settings_obj
from app.db_files.crud.meal_logs_crud import build_input_object_from_meal_log
from app.security.security import get_current_user_id
from app.db_files.crud.optimization_crud import save_optimization_macros_crud, save_optimization_weights_crud, get_optimization_macros_crud, get_optimization_weights_crud
from app.models.payload_inputs import MealTypePayload, OptimizationMacrosPayload, OptimizationWeightsPayload


router = APIRouter(prefix="/meal-optimizations", tags=["Optimization"])

"""  
Optimize a meal.
This route builds the meal input, runs optimization, saves results, and returns them.
Args:
    - meal_id (str): Target meal ID.
    - payload (MealTypePayload): Meal type for settings lookup.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Optimized weights and macros, or ingredient issues.
"""
@router.get("/{meal_id}")
async def optimize_meal(meal_id: str, payload: MealTypePayload = Depends(), user_id: str = Depends(get_current_user_id)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    input_obj, issue_list = await build_input_object_from_meal_log(meal_id, user_id) 

    if issue_list != []:   # any invalid ingredients? return early
        return {"issues": issue_list}
    
    settings_obj = await get_settings_obj(user_id=user_id, meal_type=payload.meal_type)
    if settings_obj is None:
        raise HTTPException(status_code=404, detail="User settings not found")
    
    optimization_object = linprog_optimizer(settings_obj, input_obj)

    optimization_object.solve()
    if not optimization_object.get_solution().success:
        optimization_object = gwo_optimizer(settings_obj, input_obj)
        optimization_object.solve()
    json_ingredient_weights, json_total_macros = optimization_object.get_json_results()
    await save_optimization_macros_crud(meal_id, user_id, json_total_macros)
    await save_optimization_weights_crud(meal_id, user_id, json_ingredient_weights)
    return {"weights": json_ingredient_weights, "macros": json_total_macros}



"""  
Save optimized ingredient weights.
This route stores optimization weights for the current user's meal.
Args:
    - meal_id (str): Target meal ID.
    - payload (OptimizationWeightsPayload): Optimized ingredient weights.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Save result from CRUD.
"""
@router.post("/{meal_id}/weights")
async def save_optimization_weights(meal_id: str, payload: OptimizationWeightsPayload, user_id: str = Depends(get_current_user_id) ):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    res = await save_optimization_weights_crud(meal_id, user_id, payload.root)
    if not res:
        raise HTTPException(status_code=404, detail="Meal optimization weights saving error")
    return res

"""  
Save optimized macro totals.
This route stores optimization macros for the current user's meal.
Args:
    - meal_id (str): Target meal ID.
    - payload (OptimizationMacrosPayload): Optimized macro totals.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Save result from CRUD.
"""
@router.post("/{meal_id}/macros")
async def save_optimization_macros(meal_id: str, payload: OptimizationMacrosPayload, user_id: str = Depends(get_current_user_id) ):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    res = await save_optimization_macros_crud(meal_id, user_id, payload.root)
    if not res:
        raise HTTPException(status_code=404, detail="Meal optimization macros saving error")
    return res


"""  
Get optimized macro totals.
This route returns saved macro optimization results for the current user's meal.
Args:
    - meal_id (str): Target meal ID.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Saved macro results.
"""
@router.get("/{meal_id}/macros")
async def get_optimization_macros(meal_id, user_id: str = Depends(get_current_user_id) ):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    res = await get_optimization_macros_crud(meal_id, user_id)

    return res

"""  
Get optimized ingredient weights.
This route returns saved weight optimization results for the current user's meal.
Args:
    - meal_id (str): Target meal ID.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Saved weight results.
"""
@router.get("/{meal_id}/weights")
async def get_optimization_weights(meal_id, user_id: str = Depends(get_current_user_id) ):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    res = await get_optimization_weights_crud(meal_id, user_id)

    return res

"""  
Get full optimization results.
This route returns saved weights and macros together for the current user's meal.
Args:
    - meal_id (str): Target meal ID.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Saved weights and macros.
"""
@router.get("/{meal_id}/results")
async def get_optimization_results(meal_id, user_id: str = Depends(get_current_user_id) ):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    res_weights = await get_optimization_weights_crud(meal_id, user_id)
    res_macros = await get_optimization_macros_crud(meal_id, user_id)
    return {"weights": res_weights, "macros": res_macros}
