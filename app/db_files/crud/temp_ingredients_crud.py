from app.db_files.core.database import temp_ingredients_collection
from app.db_files.models.meal_logs import MealLogModelTemp
from bson import ObjectId
from app.db_files.models.ingredient_entry import IngredientEntryTemp
from fastapi import HTTPException, status
from datetime import datetime, timezone
from pymongo.errors import PyMongoError



async def create_temp_meal( user_id: str):
    doc = MealLogModelTemp(
        user_id=user_id,
        ingredients=[]
    ).model_dump(by_alias=True, exclude_none=True)

    res = await temp_ingredients_collection.insert_one(doc)

    return await temp_ingredients_collection.find_one(
        {"_id": res.inserted_id}, {"_id": 0}
    )

async def get_temp_meal(user_id: str):
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


        

async def add_ingredient_to_temp_meal(user_id: str, ingredient: IngredientEntryTemp): 
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

async def delete_ingredient_from_temp_meal(user_id: str,  barcode: str):
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
async def fetch_temp_ingredients_list(user_id: str):

    data = await get_temp_meal(user_id)
    if not data:
        raise HTTPException(status_code=404, detail="Failed to fetch ingredient list")
    
    ingredidents = data["ingredients"]
    
    return ingredidents

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

async def return_temp_ingredients_button( user_id: str):
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


async def get_total_normalized_temp_nutrients(user_id: str):
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

async def delete_all_ingredients_from_temp(user_id: str):
    resp = await temp_ingredients_collection.update_one(
        {"user_id": user_id},
        {"$set": {"ingredients": []}}
    )
    if resp.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete ingredients")
    return resp


async def set_amount_in_temp_meal(barcode, amount, user_id):
    resp = await temp_ingredients_collection.update_one(
        {"user_id": user_id, "ingredients.barcode": barcode},
        {"$set": {"ingredients.$.amount": amount}}
    )
    if resp.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to update amount")
    return resp