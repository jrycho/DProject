from app.db_files.core.database import user_ingredients_collection, users_collection
from app.db_files.models.user_ingredient import User_IngredientDoc
from uuid import uuid4
from bson import ObjectId
from fastapi import HTTPException
import re

"""  
Get user's personal share key.
Args:
    - user_id (str): Current user ID.
Returns:
    - str: User share key.
Usage:
    - app/routes/user_functions_routes.py: get_user_key
    - Internal helper for user ingredient visibility.
Workflow:
    - Check that user_id is present.
    - Convert user_id to ObjectId.
    - Find user document.
    - Raise 404 if user does not exist.
    - Return share_key.
"""
async def get_user_key(user_id: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    resp = await users_collection.find_one({"_id": await str_to_OID(user_id)})
    if resp is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_share_key = resp["share_key"]
    return user_share_key

"""  
Get raw shared keys saved by user.
Args:
    - user_id (str): Current user ID.
Returns:
    - list: Shared keys saved on user document.
Usage:
    - Internal helper for get_user_shared_keys and get_visible_keys.
Workflow:
    - Check that user_id is present.
    - Convert user_id to ObjectId.
    - Find user document.
    - Raise 404 if user does not exist.
    - Return shared_keys list or empty list.
"""
async def get_user_shared_keys_raw(user_id: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    resp = await users_collection.find_one({"_id": await str_to_OID(user_id)})
    if resp is None:
        raise HTTPException(status_code=404, detail="User not found")
    return resp.get("shared_keys", [])

"""  
Get user's shared keys with usernames.
Args:
    - user_id (str): Current user ID.
Returns:
    - list: Shared key records with owner usernames.
Usage:
    - app/routes/user_functions_routes.py: get_user_shared_keys
Workflow:
    - Load user's saved shared keys.
    - For each key, find owning user by share_key.
    - Attach username or Unknown user.
    - Return formatted shared key list.
"""
async def get_user_shared_keys(user_id: str):
    user_shared_keys = await get_user_shared_keys_raw(user_id)
    shared_keys_with_usernames = []

    # Keep this intentionally simple: for each shared key, look up the owning user one by one.
    for shared_key in user_shared_keys:
        owner = await users_collection.find_one({"share_key": shared_key})
        shared_keys_with_usernames.append(
            {
                "shared_key": shared_key,
                "username": owner.get("username", "Unknown user") if owner else "Unknown user",
            }
        )

    return shared_keys_with_usernames

"""  
Add a shared key to user's library.
Args:
    - user_id (str): Current user ID.
    - shared_key (str): Shared key to save.
Returns:
    - UpdateResult: MongoDB update result.
Usage:
    - app/routes/user_functions_routes.py: add_key_to_library
Workflow:
    - Check that shared key exists.
    - Add shared key to user's shared_keys with $addToSet.
    - Raise 409 if key was already present.
    - Return update result.
"""
async def add_user_shared_keys(user_id: str, shared_key: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    await find_key(share_key=shared_key)
    resp = await users_collection.update_one({"_id": await str_to_OID(user_id)}, {"$addToSet": {"shared_keys": shared_key}})

    if resp.modified_count == 0:
        raise HTTPException(status_code=409, detail="Key already in the list")
    return resp


"""  
Delete a shared key from user's library.
Args:
    - user_id (str): Current user ID.
    - shared_key (str): Shared key to remove.
Returns:
    - UpdateResult: MongoDB update result.
Usage:
    - app/routes/user_functions_routes.py: delete_user_shared_key
Workflow:
    - Check that user_id is present.
    - Pull shared key from user's shared_keys list.
    - Raise 404 if key was not removed.
    - Return update result.
"""
async def delete_user_shared_key(user_id: str, shared_key: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    resp = await users_collection.update_one(
        {"_id": await str_to_OID(user_id)},
        {"$pull": {"shared_keys": shared_key}},
    )

    if resp.modified_count == 0:
        raise HTTPException(status_code=404, detail="Shared key not found")
    return resp




"""  
Create a user ingredient.
Args:
    - user_id (str): Owner of the ingredient.
    - payload (dict): Ingredient data.
Returns:
    - InsertOneResult: MongoDB insert result.
Usage:
    - app/routes/user_functions_routes.py: add_user_ingredient
    - app/routes/user_functions_routes.py: add_user_ingredient_direct
    - app/routes/user_functions_routes.py: save_temp_to_perm
Workflow:
    - Check that user_id is present.
    - Get user's share key.
    - Check ingredient name uniqueness for this user.
    - Generate custom barcode.
    - Build User_IngredientDoc.
    - Insert ingredient into user ingredients collection.
    - Return insert result.
"""
async def create_user_ingredients(user_id: str,  payload: dict):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    user_key = await get_user_key(user_id)

    if await assure_unique_name(user_id, payload.get("product_name")):
        raise HTTPException(status_code=409, detail="Ingredient name already exists")

    barcode = f"custom-{user_id}-{uuid4().hex[:8]}"
    ingredient = User_IngredientDoc(user_id=str(user_id), barcode=barcode, share_key=user_key,  **payload)
    doc = ingredient.model_dump(by_alias = True, exclude_none=True)
    resp = await user_ingredients_collection.insert_one(doc)
    return resp



"""  
Get visible user ingredient by name.
Args:
    - user_id (str): Current user ID.
    - name (str): Product name to find.
Returns:
    - dict | None: Matching ingredient document.
Usage:
    - app/routes/user_functions_routes.py: get_user_ingredient
Workflow:
    - Check that user_id is present.
    - Load keys visible to user.
    - Find ingredient by product name and visible share key.
    - Convert MongoDB _id to string.
    - Return matching document.
"""
async def get_user_ingredients(user_id: str, name: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    visible_keys = await get_visible_keys(user_id)
    doc = await user_ingredients_collection.find_one(
        {"product_name": name, "share_key": {"$in": visible_keys}}
    )
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc



"""  
Check if ingredient name already exists for user.
Args:
    - user_id (str): Current user ID.
    - name (str): Product name to check.
Returns:
    - dict | None: Existing ingredient document if found.
Usage:
    - Internal helper for create_user_ingredients.
Workflow:
    - Get user's personal share key.
    - Search ingredient with same product name and share key.
    - Return existing document or None.
"""
async def assure_unique_name(user_id: str, name: str):
    user_key = await get_user_key(user_id)
    return await user_ingredients_collection.find_one(
        {"product_name": name, "share_key": user_key}
    )



"""  
Convert string ID to ObjectId.
Args:
    - user_id (str): User ID string.
Returns:
    - ObjectId: MongoDB ObjectId.
Usage:
    - Internal helper for user document queries.
Workflow:
    - Convert user_id string to ObjectId.
    - Return ObjectId.
"""
async def str_to_OID(user_id: str):
    return ObjectId(user_id)

"""
{
  "product_name": "Test ingredient",
  "priority_user": 0,
  "nutriments": {
    "energy_kcal_100g": 250,
    "proteins_100g": 10,
    "carbohydrates_100g": 30,
    "fat_100g": 5
  },
  "categories_tags": ["test"]
}
"""

"""  
Get all share keys visible to user.
Args:
    - user_id (str): Current user ID.
Returns:
    - list: Personal share key plus saved shared keys.
Usage:
    - Internal helper for get_user_ingredients and search_crud.
Workflow:
    - Get user's personal share key.
    - Get shared keys saved by user.
    - Combine them into visible key list.
    - Return visible keys.
"""
async def get_visible_keys(user_id: str):
    user_key = await get_user_key(user_id)
    shared_keys = await get_user_shared_keys_raw(user_id)
    visible_keys = [user_key, *shared_keys]
    return visible_keys

"""  
Search visible user ingredients.
Args:
    - query: Search text.
    - user_id (str): Current user ID.
    - limit (int): Max result count.
    - skip (int): Number of results to skip.
Returns:
    - list: Matching ingredient documents.
Usage:
    - app/routes/user_functions_routes.py: search
Workflow:
    - Check that user_id is present.
    - Load keys visible to user.
    - Trim query and return empty list if blank.
    - Escape query for safe regex search.
    - Search product_name across visible share keys.
    - Convert MongoDB _id values to strings.
    - Return matching documents.
"""
async def search_crud(query, user_id: str, limit: int = 20, skip: int = 0,):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    visible_keys = await get_visible_keys(user_id)

    q = query.strip()
    if not q:
        return []
    # regex, * . + ... do special things to strings, regex avoids that with escape to search for text
    safe = re.escape(q)

    cursor = user_ingredients_collection.find(
        {
            "share_key": {"$in": visible_keys},
            "product_name": {"$regex": safe, "$options": "i"},  # contains search, case insensitive
        },
    ).skip(max(skip, 0)).limit(min(limit, 50))

    docs = await cursor.to_list(length=min(limit, 50))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs

"""  
Get one user ingredient by barcode.
Args:
    - barcode: Ingredient barcode.
Returns:
    - dict: Ingredient document.
Usage:
    - Currently no active route imports this function.
Workflow:
    - Find ingredient by code.
    - Raise 404 if ingredient does not exist.
    - Return ingredient document.
"""
async def get_user_ingredient_secure(barcode):
    doc = await user_ingredients_collection.find_one({"code": barcode})
    if doc is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return doc

"""  
Find user by share key.
Args:
    - share_key (str): Share key to validate.
Returns:
    - dict: User document owning the share key.
Usage:
    - Internal helper for add_user_shared_keys.
Workflow:
    - Find user document by share_key.
    - Raise 404 if no user owns the key.
    - Return user document.
"""
async def find_key(share_key:str):
    doc = await users_collection.find_one({"share_key": share_key})
    if doc is None:
        raise HTTPException(status_code=404, detail="Invalid key")
    return doc


"""  
Delete a user ingredient securely.
Args:
    - barcode: Ingredient barcode.
    - user_id (str): Current user ID.
Returns:
    - dict: Success message.
Usage:
    - app/routes/user_functions_routes.py: delete_user_ingredient
Workflow:
    - Check that user_id is present.
    - Find ingredient by barcode.
    - Raise 404 if ingredient does not exist.
    - Check that ingredient user_id matches current user.
    - Check that ingredient share_key matches user's share key.
    - Delete ingredient.
    - Return success message.
"""
async def delete_user_ingredient_secure(barcode, user_id: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    doc = await user_ingredients_collection.find_one({"code": barcode,})
    if doc is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    if doc["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    user_key = await get_user_key(user_id)
    if doc["share_key"] != user_key:
        raise HTTPException(status_code=403, detail="Not authorized")
    await user_ingredients_collection.delete_one({"code": barcode})
    return {"message": "Ingredient deleted"}

"""  
Initialize user shared keys.
Args:
    - user_id (str): Current user ID.
Returns:
    - UpdateResult: MongoDB update result.
Usage:
    - Currently no active route imports this function.
Workflow:
    - Add default shared key to user document.
    - Create document if it does not exist.
    - Raise 409 if update did not modify document.
    - Return update result.
"""
async def user_shared_keys_init(user_id: str):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    doc = await users_collection.update_one({"_id": user_id}, {"$addToSet": {"shared_keys": "Default_key_jghsfahpahfpjcgnpasqj32646"}}, upsert=True)
    if doc.modified_count == 0:
        raise HTTPException(status_code=409, detail="Error setting shared keys")
    return doc
