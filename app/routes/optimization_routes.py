
from fastapi import APIRouter, HTTPException

from app.optimizers.gwo_optimizer import gwo_optimizer
import app.state.state as state
from app.db_files.crud.meal_logs import build_input_object_from_meal_log

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
async def optimize_meal(meal_id: str):
    input_obj = await build_input_object_from_meal_log(meal_id)
    optimization_object = gwo_optimizer(state.session_settings, input_obj)
    optimization_object.solve()
    return optimization_object.get_json_results()