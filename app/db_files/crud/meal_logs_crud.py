from app.db_files.core.database import db
from app.db_files.models.meal_logs import MealLogModel
from datetime import datetime, timezone, date as Date
from typing import List
from app.db_files.models.ingredient_entry import IngredientEntry
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from app.models.input_obj import InputObject

from anyio.to_thread import run_sync
from uuid import uuid4
from pymongo.errors import DuplicateKeyError
from pydantic import Field
from app.db_files.crud.ingredient_crud import get_or_fetch_ingredient_dict_sync, build_ingredient
from typing import Optional
from app.models.ingredient import Ingredient
# MongoDB database and 

collection = db["meal_logs"]  # MongoDB collection

meal_logs = db.meal_logs

"""  
Create a new meal log.
Args:
    - meal_id (Optional[str]): Provided meal ID, or None to generate one.
    - user_id (str): Owner of the meal log.
    - type_of_meal (str): Meal type.
    - date (str): Meal date.
Returns:
    - str: MongoDB id of the created meal log.
Usage:
    - app/routes/meal_logs_routes.py: log_meal_with_id
    - app/routes/meal_logs_routes.py: log_meal
Workflow:
    - Use provided meal_id or create a UUID.
    - Build a MealLogModel with empty ingredients.
    - Insert it into meal_logs collection.
    - If generated ID collides, generate again.
    - If user-provided ID collides, raise 409.
"""
async def create_meal_log(meal_id: Optional[str], user_id:str, type_of_meal: str, date:str )-> str:
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
            result = await meal_logs.insert_one(meal_log.model_dump(by_alias=True, exclude_unset=True)) #insert_one, model_dump for MDB savable collection, await for work in async 
            return str(result.inserted_id) #Returning the ID of the newly inserted document as a string.
        except DuplicateKeyError:
            if meal_id:
                raise HTTPException(status_code=409, detail="Meal log with user given id already exists")
            meal_id = None
            continue
"""  
Get all meal logs.
Args:
    - None
Returns:
    - List[MealLogModel]: All meal logs in the collection.
Usage:
    - Currently no active route uses this function.
Workflow:
    - Create an empty result list.
    - Fetch every document from meal_logs.
    - Convert MongoDB _id to string.
    - Convert each document into MealLogModel.
    - Return the list.
"""


async def get_all_meal_logs() -> List[MealLogModel]:
    logs = []
    cursor = meal_logs.find({}) 
    async for doc in cursor:
        doc["_id"] = str(doc["_id"]) 
        logs.append(MealLogModel(**doc))
    return logs


"""  
Get a specific meal log by meal_id.
Args:
    - meal_id (str): Target meal ID.
    - user_id (str): Owner of the meal log.
Returns:
    - MealLogModel: Found meal log.
Usage:
    - Internal helper for build_input_object_from_meal_log.
Workflow:
    - Search meal_logs by meal_id and user_id.
    - Raise 404 if no document exists.
    - Convert MongoDB _id to string if needed.
    - Return the document as MealLogModel.
"""
async def get_meal_log_by_meal_id(meal_id: str, user_id:str):
    doc = await meal_logs.find_one({"meal_id": meal_id, "user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Meal log not found")
    if isinstance(doc.get("_id"), ObjectId):
        doc["_id"] = str(doc["_id"])
    return MealLogModel(**doc)


"""  
Add an ingredient to a meal log.
Args:
    - log_id (str): Target meal ID.
    - user_id (str): Owner of the meal log.
    - ingredient (IngredientEntry): Ingredient entry to save.
Returns:
    - dict: Success message with meal_id and barcode.
Usage:
    - app/routes/meal_logs_routes.py: add_ingredient
Workflow:
    - Convert IngredientEntry to dict.
    - Find meal log by meal_id and user_id.
    - Raise 404 if meal log does not exist.
    - Check duplicate ingredients by barcode.
    - Raise 400 if ingredient is already saved.
    - Push ingredient into meal log ingredients.
    - Raise 404 if update fails.
    - Return success response.
"""
async def add_ingredient_to_log(log_id: str, user_id: str, ingredient: IngredientEntry): #! USED
    entry_dict = ingredient.model_dump()
    
    existing_log = await meal_logs.find_one({"meal_id": log_id, "user_id": user_id})
    if not existing_log:
        raise HTTPException(status_code=404, detail="Meal log not found")
    
    if any(entry["barcode"] == entry_dict["barcode"] for entry in existing_log.get("ingredients", [])):
        raise HTTPException(status_code=400, detail="Ingredient already exists in the log")

    result = await meal_logs.update_one(
        {"meal_id": log_id, "user_id": user_id},
        {"$push": {"ingredients": entry_dict}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Meal log not found or update failed")

    return {
        "message": "Ingredient added successfully.",
        "meal_id": log_id,
        "barcode": entry_dict["barcode"],
    }
    
"""  
Build an InputObject from a meal log.
Args:
    - meal_id (str): Target meal ID.
    - user_id (str): Owner of the meal log.
Returns:
    - tuple: InputObject and list of ingredients with invalid calories.
Usage:
    - app/routes/optimization_routes.py: optimize_meal
    - Uses get_meal_log_by_meal_id internally.
Workflow:
    - Fetch meal log by meal_id and user_id.
    - Create empty InputObject and issue list.
    - Build full ingredient object for each saved ingredient entry.
    - Check if calories are numeric and positive.
    - Add invalid ingredient names to issue list.
    - Add valid ingredients to InputObject.
    - Return InputObject and issue list.
"""
async def build_input_object_from_meal_log(meal_id: str, user_id: str) -> InputObject: #! USED

    log = await get_meal_log_by_meal_id(meal_id, user_id) #loads meal
    input_object = InputObject() #object creation
    issue_list = []

    for entry in log.ingredients: #forcycle on ingredients
        ingredient = await build_ingredient(
            barcode=entry.barcode,
            priority=entry.priority,
            piece_weights=entry.piece_weight,
            set_amount=entry.set_amount,
            min_amount=entry.min_amount,
            max_amount=entry.max_amount,
        ) #calls function that fetches it from OpenFoodFacts API and build to obj needed
        cal = getattr(ingredient, "calories")
        print(cal)
        is_numeric = isinstance(cal, (int, float)) and not isinstance(cal, bool)
        if not is_numeric or cal <= 0:
            issue_list.append(getattr(ingredient, "name"))
        else:
            input_object.add_ingredient(ingredient) #input object method

    return input_object, issue_list

"""  
Delete an ingredient from a meal log.
Args:
    - meal_id (str): Target meal ID.
    - barcode (str): Ingredient barcode to remove.
    - user_id (str): Owner of the meal log.
Returns:
    - dict: Success message.
Usage:
    - app/routes/meal_logs_routes.py: remove_ingredient_by_barcode
Workflow:
    - Find meal log by meal_id and user_id.
    - Raise 404 if meal log does not exist.
    - Check if ingredient barcode exists in ingredients.
    - Raise 404 if ingredient is not in the log.
    - Pull matching ingredient from the ingredients array.
    - Raise 500 if database update fails.
    - Return success response.
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

"""  
Get meal logs for a user by date.
Args:
    - user_id (str): Owner of the meal logs.
    - date (str): Date key to match.
Returns:
    - List[MealLogModel]: JSON-compatible meal logs for that date.
Usage:
    - app/routes/meal_logs_routes.py: fetch_meal_by_date
Workflow:
    - Use the given date as the lookup key.
    - Query meal_logs by user_id and date.
    - Convert MongoDB ObjectId values to strings.
    - Return JSON-compatible list.
"""
async def get_meal_by_date(user_id: str, date: str) -> List[MealLogModel]: #! USED
    # Normalize date to only match the day (ignoring time)
    key = date

    logs = await db.meal_logs.find({
        "user_id": user_id,
        "date": key
    }).to_list(length=None)

    return jsonable_encoder(logs, custom_encoder={ObjectId: str})  # List of meal logs for that user and date


"""  
Fetch raw ingredient entries from a meal log.
Args:
    - meal_id (str): Target meal ID.
    - user_id (str): Owner of the meal log.
Returns:
    - list: Saved ingredient entries from the meal log.
Usage:
    - Internal helper for return_ingredients_button.
Workflow:
    - Find meal log by meal_id and user_id.
    - Raise 404 if ingredient list cannot be fetched.
    - Read ingredients field from the document.
    - Return ingredients list.
"""
async def fetch_ingredients_list(meal_id: str, user_id: str):

    data = await meal_logs.find_one({"meal_id": meal_id,
                                    "user_id": user_id,})
    if not data:
        raise HTTPException(status_code=404, detail="Failed to fetch ingredient list")
    
    ingredidents = data["ingredients"]
    return ingredidents

"""  
Return ingredients formatted for frontend buttons.
Args:
    - meal_id (str): Target meal ID.
    - user_id (str): Owner of the meal log.
Returns:
    - list: Ingredient button data.
Usage:
    - app/routes/meal_logs_routes.py: return_ingredients_for_buttons
    - Uses fetch_ingredients_list and ingredient_doc_to_button_json internally.
Workflow:
    - Fetch saved ingredient entries from meal log.
    - For each barcode, load ingredient data from DB or external source.
    - Convert each ingredient document into button JSON.
    - Preserve amount settings from the meal log entry.
    - Return button data list.
"""
async def return_ingredients_button(meal_id: str, user_id: str):
    barcodes_list = await fetch_ingredients_list(meal_id, user_id)
    ingredients_list = []
    ret_list = []
    for item in barcodes_list:
        ing = await get_or_fetch_ingredient_dict_sync(item["barcode"])
        ret_ing = ingredient_doc_to_button_json(
            ing,
            item.get("piece_weight", 0),
            item.get("set_amount", 0),
            item.get("min_amount", 0),
            item.get("max_amount", 0),
        )
        #print(f"ret ing {ret_ing}")
        ret_list.append(ret_ing)
        print(ret_list)
    return ret_list

"""  
Convert an ingredient document to frontend button JSON.
Args:
    - ingredient (dict): Ingredient document from DB or fetched source.
    - piece_weight: Saved piece weight.
    - set_amount: Saved set amount.
    - min_amount: Saved minimum amount.
    - max_amount: Saved maximum amount.
Returns:
    - dict: Normalized button data.
Usage:
    - Internal helper for return_ingredients_button.
    - Imported by app/routes/tracker_routes.py and app/routes/user_functions_routes.py.
Workflow:
    - Read nutrients from nutrients or nutriments field.
    - Choose display name from known name fields.
    - Choose barcode from known identifier fields.
    - Extract calories, protein, carbs, and fat.
    - Add saved amount settings.
    - Return normalized dict for frontend.
"""
def ingredient_doc_to_button_json(ingredient, piece_weight, set_amount, min_amount, max_amount):
        nutr = ingredient.get("nutrients") or ingredient.get("nutriments")
        name = ingredient.get("name") or ingredient.get("product_name") or "Unnamed"
        raw = ingredient.get("barcode") or ingredient.get("code") or ingredient.get("_id") 
        barcode = str(raw)

        kcal    = nutr.get("energy_kcal_100g") or nutr.get("energy-kcal_100g") or nutr.get("energy_kcal") or nutr.get("energy-kcal") or 0
        protein = nutr.get("proteins_100g")    or nutr.get("protein_100g")      or nutr.get("proteins")     or 0
        carbs   = nutr.get("carbohydrates_100g") or nutr.get("carbs_100g")     or nutr.get("carbohydrates") or 0
        fat     = nutr.get("fat_100g")         or nutr.get("fats_100g")         or nutr.get("fat")  
        
        ret_dict = {
        "name": name,
        "kcal": (kcal),
        "protein": (protein),
        "carbs": (carbs),
        "fat": (fat),
        "barcode": barcode,

        "piece_weight": piece_weight,
        "set_amount": set_amount,
        "min_amount": min_amount,
        "max_amount": max_amount,
    }
        return ret_dict

"""  
Update amount settings for one meal ingredient.
Args:
    - meal_id (str): Target meal ID.
    - user_id (str): Owner of the meal log.
    - barcode (str): Ingredient barcode.
    - set_amount (Optional[float]): Saved set amount.
    - piece_weight (Optional[float]): Saved piece weight.
    - min_amount (Optional[float]): Saved minimum amount.
    - max_amount (Optional[float]): Saved maximum amount.
Returns:
    - dict: Update result.
Usage:
    - app/routes/meal_logs_routes.py: update_ingredient_amount_settings
Workflow:
    - Match meal log by meal_id, user_id, and ingredient barcode.
    - Set amount fields on the matched ingredient array item.
    - Raise 404 if meal or ingredient is not found.
    - Return ok response.
"""
async def update_ingredient_amount_settings_crud(
    meal_id: str,
    user_id: str,
    barcode: str,
    set_amount: Optional[float] = None,
    piece_weight: Optional[float] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
):

    result = await meal_logs.update_one(
        {
            "meal_id": meal_id,
            "user_id": user_id,
            "ingredients.barcode": barcode,
        },
        {
            "$set": {
                "ingredients.$.set_amount": set_amount,
                "ingredients.$.piece_weight": piece_weight,
                "ingredients.$.min_amount": min_amount,
                "ingredients.$.max_amount": max_amount,
            }
        },
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Meal or ingredient not found")

    return {"ok": True}

