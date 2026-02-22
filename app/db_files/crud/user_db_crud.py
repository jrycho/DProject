from app.db_files.core.database import user_ingredients_collection, user_meals_collection, users_collection
from app.db_files.models.user_ingredient import User_IngredientDoc
from uuid import uuid4
from bson import ObjectId
from fastapi import HTTPException
import logging
import re

log = logging.getLogger(__name__)

async def get_user_key(user_id: str):

    resp = await users_collection.find_one({"_id": await str_to_OID(user_id)})
    if resp is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_share_key = resp["share_key"]
    return user_share_key

async def get_user_shared_keys(user_id: str):
    resp = await users_collection.find_one({"_id": await str_to_OID(user_id)})
    user_shared_keys = resp["shared_keys"]
    return user_shared_keys

async def add_user_shared_keys(user_id: str, shared_key: str):
    await find_key(share_key=shared_key)
    resp = await users_collection.update_one({"_id": await str_to_OID(user_id)}, {"$addToSet": {"shared_keys": shared_key}})

    if resp.modified_count == 0:
        raise HTTPException(status_code=409, detail="Key already in the list")
    return resp




async def create_user_ingredients(user_id: str,  payload: dict):
    user_key = await get_user_key(user_id)

    if await assure_unique_name(user_id, payload.get("product_name")):
        raise HTTPException(status_code=409, detail="Ingredient name already exists")

    barcode = f"custom-{user_id}-{uuid4().hex[:8]}"
    ingredient = User_IngredientDoc(user_id=str(user_id), barcode=barcode, share_key=user_key,  **payload)
    doc = ingredient.model_dump(by_alias = True)
    resp = await user_ingredients_collection.insert_one(doc)
    return resp



async def get_user_ingredients(user_id: str, name: str):

    visible_keys = await get_visible_keys(user_id)
    doc = await user_ingredients_collection.find_one(
        {"product_name": name, "share_key": {"$in": visible_keys}}
    )
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc



async def assure_unique_name(user_id: str, name: str):
    user_key = await get_user_key(user_id)
    return await user_ingredients_collection.find_one(
        {"product_name": name, "share_key": user_key}
    )



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

async def get_visible_keys(user_id: str):
    user_key = await get_user_key(user_id)
    shared_keys = await get_user_shared_keys(user_id)
    visible_keys = [user_key, *shared_keys]
    return visible_keys

async def search_crud(query, user_id: str, limit: int = 20, skip: int = 0,):
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

async def get_user_ingredient_secure(barcode):
    doc = await user_ingredients_collection.find_one({"code": barcode})
    if doc is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return doc

async def find_key(share_key:str):
    doc = await users_collection.find_one({"share_key": share_key})
    if doc is None:
        raise HTTPException(status_code=404, detail="Invalid key")
    return doc