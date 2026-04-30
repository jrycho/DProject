from app.db_files.core.database import temp_ingredients_collection
from app.db_files.models.meal_logs import MealLogModelTemp
from bson import ObjectId
from app.db_files.models.ingredient_entry import IngredientEntryTemp
from fastapi import HTTPException, status
from datetime import datetime, timezone
from pymongo.errors import PyMongoError


"""  
Create a temporary meal document.
Args:
    - user_id (str): Owner of the temporary meal.
Returns:
    - dict: Created temporary meal document without MongoDB _id.
Usage:
    - app/routes/user_functions_routes.py: add_ingredient_to_temp_log
    - Internal helper for get_temp_meal.
Workflow:
    - Check that user_id is present.
    - Build empty MealLogModelTemp.
    - Insert it into temp ingredients collection.
    - Fetch and return the created document.
"""
async def create_temp_meal( user_id: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    doc = MealLogModelTemp(
        user_id=user_id,
        ingredients=[]
    ).model_dump(by_alias=True, exclude_none=True)

    res = await temp_ingredients_collection.insert_one(doc)

    return await temp_ingredients_collection.find_one(
        {"_id": res.inserted_id}, {"_id": 0}
    )

"""  
Get the current user's temporary meal.
Args:
    - user_id (str): Owner of the temporary meal.
Returns:
    - dict: Temporary meal document.
Usage:
    - app/routes/user_functions_routes.py: add_ingredient_to_temp_log
    - Internal helper for add_ingredient_to_temp_meal and fetch_temp_ingredients_list.
Workflow:
    - Check that user_id is present.
    - Try to find existing temp meal.
    - Create temp meal if none exists.
    - Return temp meal document.
"""
async def get_temp_meal(user_id: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    try:
        doc = await temp_ingredients_collection.find_one(
        {"user_id": user_id}, {"_id": 0}
        )

    except PyMongoError as e:
        raise RuntimeError(f"Database read failed: {e}")

    if doc is None:
        try:
            doc = await create_temp_meal(user_id)
        except PyMongoError as e:
            raise RuntimeError(f"Database read failed: {e}")
    return doc


        

"""  
Add or update ingredient in temporary meal.
Args:
    - user_id (str): Owner of the temporary meal.
    - ingredient (IngredientEntryTemp): Ingredient to save.
Returns:
    - dict: Updated temporary meal document.
Usage:
    - app/routes/user_functions_routes.py: add_ingredient_to_temp_log
Workflow:
    - Check that user_id is present.
    - Load or create user's temp meal.
    - Replace existing ingredient with same barcode.
    - Add ingredient if barcode is not already present.
    - Save updated ingredients list.
    - Return updated temp meal.
"""
async def add_ingredient_to_temp_meal(user_id: str, ingredient: IngredientEntryTemp): 
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    doc = await get_temp_meal(user_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    
    items = doc.get("ingredients", [])

    for i, it in enumerate(items):
        if it["barcode"] == ingredient.barcode:
            # update existing
            items[i] = ingredient.model_dump(by_alias=True)
            break
    else:
        # not found → add new
        items.append(ingredient.model_dump(by_alias=True))
    

    await temp_ingredients_collection.update_one(
        {"user_id": user_id},
        {"$set": {"ingredients": items}}
    )
    return await get_temp_meal(user_id=user_id)

"""  
Delete ingredient from temporary meal.
Args:
    - user_id (str): Owner of the temporary meal.
    - barcode (str): Ingredient barcode to remove.
Returns:
    - dict: Delete result.
Usage:
    - app/routes/user_functions_routes.py: delete_ingredient_from_temp_log
Workflow:
    - Check that user_id is present.
    - Pull ingredient with matching barcode from temp meal.
    - Raise 404 if no ingredient was removed.
    - Return ok response.
"""
async def delete_ingredient_from_temp_meal(user_id: str,  barcode: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    res = await temp_ingredients_collection.update_one(
        {"user_id": user_id},
        {
            "$pull": {
                "ingredients": {"barcode": barcode}
            }
        }
    )


    if res.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found",
        )

    return {"ok": True}

#****************************************************************************************************************
from app.db_files.crud.ingredient_crud import get_or_fetch_ingredient_dict_sync

"""  
Fetch raw temporary ingredient entries.
Args:
    - user_id (str): Owner of the temporary meal.
Returns:
    - list: Saved temporary ingredient entries.
Usage:
    - Internal helper for return_temp_ingredients_button and get_total_normalized_temp_nutrients.
Workflow:
    - Check that user_id is present.
    - Load user's temp meal.
    - Raise 404 if ingredient list cannot be fetched.
    - Return ingredients list.
"""
async def fetch_temp_ingredients_list(user_id: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    data = await get_temp_meal(user_id)
    if not data:
        raise HTTPException(status_code=404, detail="Failed to fetch ingredient list")
    
    ingredidents = data["ingredients"]
    
    return ingredidents

"""  
Convert ingredient document to temporary button JSON.
Args:
    - ingredient (dict): Ingredient document from DB or fetched source.
    - amount: Saved ingredient amount.
Returns:
    - dict: Normalized ingredient button data.
Usage:
    - Internal helper for return_temp_ingredients_button.
Workflow:
    - Read nutrients from nutrients or nutriments field.
    - Choose name and barcode from known fields.
    - Extract calories, protein, carbs, and fat.
    - Add saved amount.
    - Return frontend-ready dict.
"""
def ingredient_doc_to_button_json(ingredient, amount):
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

        "amount": amount
    }
        return ret_dict

"""  
Return temporary ingredients formatted for frontend buttons.
Args:
    - user_id (str): Owner of the temporary meal.
Returns:
    - list: Temporary ingredient button data.
Usage:
    - app/routes/user_functions_routes.py: fetch_temp_ingredients_buttons
Workflow:
    - Check that user_id is present.
    - Fetch raw temp ingredient entries.
    - Load each ingredient document by barcode.
    - Convert each ingredient to button JSON.
    - Return button list.
"""
async def return_temp_ingredients_button( user_id: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    barcodes_list = await fetch_temp_ingredients_list( user_id)
    print(barcodes_list)

    ret_list = []
    for item in barcodes_list:
        ing = await get_or_fetch_ingredient_dict_sync(item["barcode"])
        ret_ing = ingredient_doc_to_button_json(ing, item.get("amount", 0))
        #print(f"ret ing {ret_ing}")
        ret_list.append(ret_ing)
    return ret_list
#****************************************************************************************************************


"""  
Calculate normalized nutrients for temporary ingredients.
Args:
    - user_id (str): Owner of the temporary meal.
Returns:
    - dict: Nutrients normalized per 100 grams.
Usage:
    - app/routes/user_functions_routes.py: save_temp_to_perm
Workflow:
    - Check that user_id is present.
    - Fetch temp ingredient entries.
    - Load ingredient documents and amounts.
    - Sum nutrients by ingredient amount.
    - Normalize totals per 100 grams.
    - Return normalized nutrient dict.
"""
async def get_total_normalized_temp_nutrients(user_id: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # 1 build ingredients in temp collection
    barcodes_list = await fetch_temp_ingredients_list(user_id)
    ingredients_list = []
    amounts_list = []
    for item in barcodes_list:
        ing = await get_or_fetch_ingredient_dict_sync(item["barcode"])

        ingredients_list.append(ing)
        amounts_list.append(item.get("amount"))
    
    # 2 add up nutriments
    total_macros = sum_all_nutrients(ingredients_list, amounts_list)

    # 3 add up amounts
    total_amount = sum(amounts_list)
    # 4 save to permanent collection
    ret_dict = {}
    for key, value in total_macros.items():
        try:
            ret_dict[key] = value/(total_amount) * 100.0
        except (TypeError, ValueError):
            continue
    # 5 save to permanent collection

    return ret_dict

"""  
Sum nutrients for ingredient documents and amounts.
Args:
    - ingredients_list: Ingredient documents.
    - amounts_list: Amounts matching ingredient list positions.
Returns:
    - dict: Summed nutrient totals.
Usage:
    - Internal helper for get_total_normalized_temp_nutrients.
Workflow:
    - Iterate ingredients and matching amounts by index.
    - Convert amount to per-100g factor.
    - Iterate nutrient values.
    - Add numeric nutrient values into totals.
    - Return totals.
"""
def sum_all_nutrients(ingredients_list, amounts_list):
    ret_dict = {}
    #index, object
    for i, ing in enumerate(ingredients_list):
        factor = amounts_list[i] / 100.0

        nutr = ing.get("nutrients", {})
        #get key, get value
        for key, value in nutr.items():
            print(key ,value)
            try:
                val = float(value)
                print(val)
            except (TypeError, ValueError):
                continue

            ret_dict[key] = ret_dict.get(key, 0.0) + val * factor

    return ret_dict

"""  
Delete all temporary ingredients.
Args:
    - user_id (str): Owner of the temporary meal.
Returns:
    - UpdateResult: MongoDB update result.
Usage:
    - app/routes/user_functions_routes.py: save_temp_to_perm
Workflow:
    - Check that user_id is present.
    - Set temp ingredients list to empty.
    - Raise 404 if update did not modify a document.
    - Return update result.
"""
async def delete_all_ingredients_from_temp(user_id: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    resp = await temp_ingredients_collection.update_one(
        {"user_id": user_id},
        {"$set": {"ingredients": []}}
    )
    if resp.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete ingredients")
    return resp


"""  
Set amount for one temporary ingredient.
Args:
    - barcode: Ingredient barcode.
    - amount: New amount value.
    - user_id: Owner of the temporary meal.
Returns:
    - UpdateResult: MongoDB update result.
Usage:
    - app/routes/user_functions_routes.py: set_amount_in_temp_
Workflow:
    - Check that user_id is present.
    - Match temp meal by user_id and ingredient barcode.
    - Set amount on the matched ingredient array item.
    - Raise 404 if no document was modified.
    - Return update result.
"""
async def set_amount_in_temp_meal(barcode, amount, user_id):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    resp = await temp_ingredients_collection.update_one(
        {"user_id": user_id, "ingredients.barcode": barcode},
        {"$set": {"ingredients.$.amount": amount}}
    )
    if resp.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to update amount")
    return resp
