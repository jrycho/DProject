from app.db_files.core.database import optimized_macros_collection, optimized_weights_collection
from fastapi import HTTPException
from datetime import datetime
from pymongo.errors import PyMongoError

def optimisation_sanity_check(input_list):
    pass

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


async def get_optimization_weights_crud(meal_id, user_id):
    data = await optimized_weights_collection.find_one({"user_id": user_id},{"meal_id":meal_id})
                                             
    if not data:
        raise HTTPException(status_code=404, detail="Weights not found")
    return data

async def get_optimization_macros_crud(meal_id, user_id):
    data = await optimized_macros_collection.find_one({"user_id": user_id},{"meal_id":meal_id})
                                             
    if not data:
        raise HTTPException(status_code=404, detail="Macros not found")
    return data
