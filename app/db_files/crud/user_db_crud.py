from app.db_files.core.database import user_inggredients_collection, user_meals_collection, users_collection
from app.db_files.models.user_ingredient import User_IngredientDoc
from uuid import uuid4
from bson import ObjectId
from fastapi import HTTPException
import logging

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

    resp = await users_collection.update_one({"_id": await str_to_OID(user_id)}, {"$addToSet": {"shared_keys": shared_key}})

    if resp.modified_count == 0:
        raise HTTPException(status_code=401, detail="Key already in the list")
    return resp


async def create_user_ingredients(user_id: str,  payload: dict):
    user_key = await get_user_key(user_id)
    barcode = f"custom-{user_id}-{uuid4().hex[:8]}"
    ingredient = User_IngredientDoc(user_id=str(user_id), barcode=barcode, share_key=user_key,  **payload)
    doc = ingredient.model_dump(by_alias = True)
    res = await user_inggredients_collection.insert_one(doc)
    return res.inserted_id

async def get_user_ingredients(user_id: str, name: str):
    user_key = await get_user_key(user_id)
    shared_keys = await get_user_shared_keys(user_id)
    visible_keys = [user_key, *shared_keys]
    return await user_inggredients_collection.find_one({"name":name, "share_key": {"$in": visible_keys}}) 

async def str_to_OID(user_id: str):
    return ObjectId(user_id)