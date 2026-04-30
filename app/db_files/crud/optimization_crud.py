from app.db_files.core.database import optimized_macros_collection, optimized_weights_collection
from fastapi import HTTPException
from datetime import datetime
from pymongo.errors import PyMongoError

MACROS_PLACEHOLDER = {"No macros yet": "-"}  # object (dict)

WEIGHTS_PLACEHOLDER = [
    {
        "barcode": "Placeholder",
        "name": "No items",
        "grams": "-"
    }
]

"""  
Optimization sanity check placeholder.
Args:
    - input_list: Optimization input data.
Returns:
    - None
Usage:
    - Currently no active call site found in app/.
Workflow:
    - Placeholder for future validation before optimization.
    - Not implemented yet.
"""
def optimisation_sanity_check(input_list):
    pass

"""  
Save optimized ingredient weights.
Args:
    - meal_id: Target meal ID.
    - user_id: Owner of the meal.
    - payload: Optimized ingredient weights.
Returns:
    - UpdateResult: MongoDB update result.
Usage:
    - app/routes/optimization_routes.py: optimize_meal
    - app/routes/optimization_routes.py: save_optimization_weights
Workflow:
    - Match saved weights by meal_id and user_id.
    - Store meal_id, user_id, and optimization results.
    - Create the document if it does not exist.
    - Convert database errors to HTTP 500.
    - Return MongoDB update result.
"""
async def save_optimization_weights_crud(meal_id, user_id, payload):
    try:
        res = await optimized_weights_collection.update_one(
            {"meal_id": meal_id, "user_id": user_id},
            {
                "$set": {
                    "meal_id": meal_id,
                    "user_id": user_id,
                    "results": payload,
                    },
                    "$setOnInsert": {
                    },
                },
                upsert=True,
            )
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e.__class__.__name__}")
    return res


"""  
Save optimized macro totals.
Args:
    - meal_id: Target meal ID.
    - user_id: Owner of the meal.
    - payload: Optimized macro totals.
Returns:
    - UpdateResult: MongoDB update result.
Usage:
    - app/routes/optimization_routes.py: optimize_meal
    - app/routes/optimization_routes.py: save_optimization_macros
Workflow:
    - Match saved macros by meal_id and user_id.
    - Store meal_id, user_id, and optimization results.
    - Create the document if it does not exist.
    - Convert database errors to HTTP 500.
    - Return MongoDB update result.
"""
async def save_optimization_macros_crud(meal_id, user_id, payload):
    try:
        res = await optimized_macros_collection.update_one(
                {"meal_id": meal_id, "user_id": user_id},
                {
                    "$set": {
                        "meal_id": meal_id,
                        "user_id": user_id,
                        "results": payload,
                    },
                    "$setOnInsert": {
                    },
                },
                upsert=True,
            )
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e.__class__.__name__}")
    return res


"""  
Get optimized ingredient weights.
Args:
    - meal_id: Target meal ID.
    - user_id: Owner of the meal.
Returns:
    - list: Saved weights, or placeholder if no results exist.
Usage:
    - app/routes/optimization_routes.py: get_optimization_weights
    - app/routes/optimization_routes.py: get_optimization_results
Workflow:
    - Query saved weights by meal_id and user_id.
    - Only return the results field.
    - Return placeholder when no saved results exist.
    - Return saved weight results otherwise.
"""
async def get_optimization_weights_crud(meal_id, user_id):
    data = await optimized_weights_collection.find_one({"user_id": user_id,"meal_id":meal_id},{"_id": 0, "results": 1})
                                             
    if not data or "results" not in data:
        return WEIGHTS_PLACEHOLDER
    return data["results"]

"""  
Get optimized macro totals.
Args:
    - meal_id: Target meal ID.
    - user_id: Owner of the meal.
Returns:
    - dict: Saved macros, or placeholder if no results exist.
Usage:
    - app/routes/optimization_routes.py: get_optimization_macros
    - app/routes/optimization_routes.py: get_optimization_results
Workflow:
    - Query saved macros by meal_id and user_id.
    - Only return the results field.
    - Return placeholder when no saved results exist.
    - Return saved macro results otherwise.
"""
async def get_optimization_macros_crud(meal_id, user_id):
    data = await optimized_macros_collection.find_one({"user_id": user_id,"meal_id":meal_id},{"_id": 0, "results": 1})
                                             
    if not data or "results" not in data:
        return MACROS_PLACEHOLDER
    return data["results"]
