from app.db_files.core.database import db
from app.db_files.models.meal_logs import MealLogModel
from datetime import datetime, timezone, date as Date
from typing import List
from app.db_files.models.ingredient_entry import IngredientEntry
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from app.models.input_obj import InputObject
from app.utils.build_ingredient_from_barcode import build_ingredient_from_barcode, build_ingredient_from_db
from anyio.to_thread import run_sync
from uuid import uuid4
from pymongo.errors import DuplicateKeyError
from pydantic import Field
from app.db_files.crud.ingredient_crud import get_or_fetch_ingredient_dict_sync
# MongoDB database and 
collection = db["meal_logs"]  # MongoDB collection

meal_logs = db.meal_logs

"""  
Create a new meal log
args: meal_id: str
creates meal log via MealLogModel class
returns: str (id of the new meal log)

"""
async def create_meal_log(meal_id: str | None, user_id:str, type_of_meal: str, date:str )-> str:
 while True:
        internal_meal_id = meal_id or str(uuid4())
        meal_log = MealLogModel(
            meal_id=internal_meal_id,
            user_id = user_id,
            type_of_meal=type_of_meal,
            date = date,
            ingredients= [],
        )
        try:
            result = await collection.insert_one(meal_log.model_dump(by_alias=True, exclude_unset=True)) #insert_one, model_dump for MDB savable collection, await for work in async 
            return str(result.inserted_id) #Returning the ID of the newly inserted document as a string.
        except DuplicateKeyError:
            if meal_id:
                raise HTTPException(status_code=409, detail="Meal log with user given id already exists")
            meal_id = None
            continue
"""  
Get all meal logs (can filter by user_id later)
creates list
find all documents in the collection
converts MDB id to string
appends MealLogModelto list
returns it
"""


async def get_all_meal_logs() -> List[MealLogModel]:
    logs = []
    cursor = collection.find({}) 
    async for doc in cursor:
        doc["_id"] = str(doc["_id"]) 
        logs.append(MealLogModel(**doc))
    return logs


"""  
Get a specific meal log by meal_id
args: meal_id: str, user_id: str
Finds a document in the meal_logs collection with given meal_id
Raises 404 if not found
Returns it as a MealLogModel
"""
async def get_meal_log_by_meal_id(meal_id: str, user_id:str):
    doc = await meal_logs.find_one({"meal_id": meal_id, "user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Meal log not found")
    if isinstance(doc.get("_id"), ObjectId):
        doc["_id"] = str(doc["_id"])
    return MealLogModel(**doc)


"""  
Add an ingredient to a meal log
args: barcode: str, priority: str
Converts ingredient to dict
Finds meal log by log_id
Raises 404 if log not found
Checks if ingredient already exists (by barcode)
Raises 400 if duplicate
Pushes ingredient to log's ingredients list
Raises 404 if update fails
"""
async def add_ingredient_to_log(log_id: str, ingredient: IngredientEntry): #! USED
    entry_dict = ingredient.model_dump()
    
    existing_log = await meal_logs.find_one({"meal_id": log_id})
    if not existing_log:
        raise HTTPException(status_code=404, detail="Meal log not found")
    
    if any(entry["barcode"] == entry_dict["barcode"] for entry in existing_log.get("ingredients", [])):
        raise HTTPException(status_code=400, detail="Ingredient already exists in the log")

    result = await meal_logs.update_one(
        {"meal_id": log_id},
        {"$push": {"ingredients": entry_dict}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Meal log not found or update failed")
    
"""  
Builds an InputObject from a meal log
Fetches meal log by meal_id
For each ingredient:
    Uses run_sync to create ingredient object (from barcode and priority)
    Adds it to the input object
Returns the InputObject
"""
async def build_input_object_from_meal_log(meal_id: str, user_id: str) -> InputObject: #! USED

    log = await get_meal_log_by_meal_id(meal_id, user_id) #loads meal
    input_object = InputObject() #object creation

    for entry in log.ingredients: #forcycle on ingredients
        ingredient = await run_sync(build_ingredient_from_barcode, entry.barcode, entry.priority) #calls function that fetches it from OpenFoodFacts API and build to obj needed
        input_object.add_ingredient(ingredient) #input object method

    return input_object
        
"""  
Delete an ingredient from a meal log
Finds meal log by meal_id
Raises 404 if not found
Checks if ingredient with given barcode exists
Raises 404 if not found
Uses $pull to remove ingredient from log
Raises 500 if update fails
Returns success message
"""
async def delete_ingredient_from_meal_log(meal_id, barcode, user_id):
    doc = await meal_logs.find_one({"meal_id": meal_id,
                                    "user_id": user_id,})
    if not doc:
        raise HTTPException(status_code=404, detail="Meal log not found")
    
    ingredients = doc.get("ingredients", [])
    if not any(entry["barcode"] == barcode for entry in ingredients): #oneline iteration through list
        raise HTTPException(status_code=404, detail="Ingredient not found in the log")
    
    result = await meal_logs.update_one(
        {"meal_id": meal_id,
        "user_id": user_id},
        {"$pull": {"ingredients": {"barcode": barcode}}}
    )
    #HTTP messages wanking
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to remove ingredient from log")
    
    return {"message": f"Ingredient {barcode} removed from meal {meal_id}"}

async def get_meal_by_date(user_id: str, date: str) -> List[MealLogModel]: #! USED
    # Normalize date to only match the day (ignoring time)
    key = date

    logs = await db.meal_logs.find({
        "user_id": user_id,
        "date": key
    }).to_list(length=None)

    return jsonable_encoder(logs, custom_encoder={ObjectId: str})  # List of meal logs for that user and date


async def fetch_ingredients_list(meal_id: str, user_id: str):

    data = await meal_logs.find_one({"meal_id": meal_id,
                                    "user_id": user_id,})
    if not data:
        raise HTTPException(status_code=404, detail="Failed to fetch ingredient list")
    
    ingredidents = data["ingredients"]
    return ingredidents

async def return_ingredients_button(meal_id: str, user_id: str):
    barcodes_list = await fetch_ingredients_list(meal_id, user_id)
    ingredients_list = []
    ret_list = []
    for item in barcodes_list:
        ing = await get_or_fetch_ingredient_dict_sync(item["barcode"])
        ret_ing = ingredient_doc_to_button_json(ing)
        print(f"ret ing {ret_ing}")
        ret_list.append(ret_ing)
    return ret_list

def ingredient_doc_to_button_json(ingredient):
    
        ret_dict = {
        "name": ingredient.get("product_name") or "Unnamed",
        "kcal": proofing(ingredient.get("energy_kcal")),
        "protein":proofing(ingredient.get("proteins_100g")),
        "carbs": proofing(ingredient.get("carbohydrates_100g")),
        "fat": proofing(ingredient.get("fat_100g")),
        "barcode": ingredient.get("barcode"),}
        return ret_dict

def proofing(x):
    if x is None or x =="":
        return 0.0
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0