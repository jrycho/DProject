from fastapi import APIRouter, HTTPException, Depends

from app.optimizers.gwo_optimizer import gwo_optimizer
from app.optimizers.linprog_optimizer import linprog_optimizer
from app.db_files.crud.settings_saves import get_settings_obj
from app.db_files.crud.meal_logs_crud import build_input_object_from_meal_log
from app.security.security import get_current_user_id
from app.db_files.crud.optimization import save_optimization_macros_crud, save_optimization_weights_crud, get_optimization_macros_crud, get_optimization_weights_crud
from app.models.payload_inputs import MealTypePayload, OptimizationMacrosPayload, OptimizationWeightsPayload


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
async def optimize_meal(meal_id: str, payload: MealTypePayload = Depends(), user_id: str = Depends(get_current_user_id)):
    input_obj, issue_list = await build_input_object_from_meal_log(meal_id, user_id) 
    print("got somewhere 1")
    print(issue_list)

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
    print(json_ingredient_weights)
    print(json_total_macros)
    await save_optimization_macros_crud(meal_id, user_id, json_total_macros)
    await save_optimization_weights_crud(meal_id, user_id, json_ingredient_weights)
    return {"weights": json_ingredient_weights, "macros": json_total_macros}




@router.post("/optimize/save_optimization_weights/{meal_id}")
async def save_optimization_weights(meal_id: str, payload: OptimizationWeightsPayload, user_id: str = Depends(get_current_user_id) ):
    res = await save_optimization_weights_crud(meal_id, user_id, payload.root)
    if not res:
        raise HTTPException(status_code=404, detail="Meal optimization weights saving error")
    return res

@router.post("/optimize/save_optimization_macros/{meal_id}")
async def save_optimization_macros(meal_id: str, payload: OptimizationMacrosPayload, user_id: str = Depends(get_current_user_id) ):
    res = await save_optimization_macros_crud(meal_id, user_id, payload.root)
    if not res:
        raise HTTPException(status_code=404, detail="Meal optimization macros saving error")
    return res


MACROS_PLACEHOLDER = {"No macros yet": "-"}

@router.get("/optimize/get_optimization_macros/{meal_id}")
async def get_optimization_macros(meal_id, user_id: str = Depends(get_current_user_id) ):
    res = await get_optimization_macros_crud(meal_id, user_id)

    return res

WEIGHTS_PLACEHOLDER = [
    { "name": "No items", "grams": "-"}
]
@router.get("/optimize/get_optimization_weights/{meal_id}")
async def get_optimization_weights(meal_id, user_id: str = Depends(get_current_user_id) ):
    res = await get_optimization_weights_crud(meal_id, user_id)

    return res

@router.get("/optimize/get_optimization_macros_and_weights/{meal_id}")
async def get_optimization_macros(meal_id, user_id: str = Depends(get_current_user_id) ):
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    res_weights = await get_optimization_weights_crud(meal_id, user_id)
    res_macros = await get_optimization_macros_crud(meal_id, user_id)
    return {"weights": res_weights, "macros": res_macros}
