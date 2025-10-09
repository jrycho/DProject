from fastapi import APIRouter, HTTPException, Depends

from app.optimizers.gwo_optimizer import gwo_optimizer
from app.db_files.crud.settings_saves import get_settings_obj
from app.db_files.crud.meal_logs import build_input_object_from_meal_log
from app.security.security import get_current_user_id

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
    input_obj = await build_input_object_from_meal_log(meal_id, user_id)
    settings_obj = await get_settings_obj(user_id)
    optimization_object = gwo_optimizer(settings_obj, input_obj)
    optimization_object.solve()
    return optimization_object.get_json_results()