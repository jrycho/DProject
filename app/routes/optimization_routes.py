from fastapi import APIRouter, HTTPException, Depends

from app.optimizers.gwo_optimizer import gwo_optimizer
from app.db_files.crud.settings_saves import get_settings_obj
from app.db_files.crud.meal_logs import build_input_object_from_meal_log
from app.security.security import get_current_user_id
from app.db_files.crud.optimization import save_optimization_macros_crud, save_optimization_weights_crud, get_optimization_macros_crud, get_optimization_weights_crud


router = APIRouter(prefix="/optim", tags=["Optimization"])

"""  
Optimize meal
args: meal_id: str

builds input object from meal_log
calls optimization algorithm with settings in state
calls solver
returns results in JSON form, not saved, user result, if needed could be optimized again for same result
"""
@router.get("/optimize/{meal_id}")
async def optimize_meal(meal_id: str, user_id: str = Depends(get_current_user_id)):
    input_obj, issue_list = await build_input_object_from_meal_log(meal_id, user_id) 
    print("got somewhere 1")
    print(issue_list)

    if issue_list != []:   # any invalid ingredients? return early
        return {"issues": issue_list}
    
    settings_obj = await get_settings_obj(user_id)
    if settings_obj is None:
        raise HTTPException(status_code=404, detail="User settings not found")
    
    optimization_object = gwo_optimizer(settings_obj, input_obj)

    optimization_object.solve()
    json_ingredient_weights, json_total_macros = optimization_object.get_json_results()
    print(json_ingredient_weights)
    print(json_total_macros)
    await save_optimization_macros_crud(meal_id, user_id, json_total_macros)
    await save_optimization_weights_crud(meal_id, user_id, json_ingredient_weights)
    return json_ingredient_weights, json_total_macros




@router.post("/optimize/save_optimization_weights/{meal_id}")
async def save_optimization_weights(meal_id, json, user_id: str = Depends(get_current_user_id) ):
    res = await save_optimization_weights_crud(meal_id, user_id, json)
    if not res:
        raise HTTPException(status_code=404, detail="Meal optimization weights saving error")
    return res

@router.post("/optimize/save_optimization_macros/{meal_id}")
async def save_optimization_macros(meal_id, json, user_id: str = Depends(get_current_user_id) ):
    res = await save_optimization_macros_crud(meal_id, user_id, json)
    if not res:
        raise HTTPException(status_code=404, detail="Meal optimization macros saving error")
    return res

@router.get("/optimize/get_optimization_macros/{meal_id}")
async def get_optimization_macros(meal_id, user_id: str = Depends(get_current_user_id) ):
    res = await get_optimization_macros_crud(meal_id, user_id)
    if not res:
        raise HTTPException(status_code=404, detail="Meal optimization macros not found")
    return res

@router.get("/optimize/get_optimization_weights/{meal_id}")
async def get_optimization_weights(meal_id, user_id: str = Depends(get_current_user_id) ):
    res = await get_optimization_weights_crud(meal_id, user_id)
    if not res:
        raise HTTPException(status_code=404, detail="Meal optimization macros not found")
    return res