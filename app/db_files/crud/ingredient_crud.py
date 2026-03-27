import requests
import httpx
from app.db_files.core.database import ingredients_collection
from fastapi import HTTPException
from app.db_files.models.ingredient_entry import IngredientEntry
from app.db_files.models.ingredient import IngredientDoc
from app.models.ingredient import Ingredient
from app.db_files.crud.user_db_crud import get_user_ingredient_secure

def _norm_tags(xs): #! USED
    """
    Normalize OFF tag arrays like:
        ["en:snacks", "cs:sladkosti"] -> ["snacks", "sladkosti"]

    - Handles None by treating it as [].
    - Keeps only strings.
    - Lowercases and strips language prefixes before ':'.
    """
    return [x.split(":")[-1].lower() for x in (xs or []) if isinstance(x, str)]


async def off_fetch_product(barcode: str) -> dict: #! USED
    """
    Fetch a product from Open Food Facts (OFF) by barcode.

    Returns:
        product (dict): OFF "product" object (raw OFF schema)

    Raises:
        HTTPException:
            - If OFF API fails (non-200)
            - If product is missing (404)

    NOTE (important):
        Using `requests.get()` inside `async def` blocks the event loop.
        So we use `httpx.AsyncClient()` instead.
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    barcode = str(barcode).strip()
    
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Open Food Facts API failed")

    data = response.json()
    product = data.get("product")
    print(data)


    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    return product

async def get_ingredient(barcode):  #! USED
    """
    Get one ingredient from Mongo by barcode.

    Storage convention here:
        - Mongo `_id` == barcode
        - The document also contains "barcode": <barcode>

    Returns:
        dict without `_id` field (projection removes it),
        or None if not found.
    """
    return await ingredients_collection.find_one({"_id":barcode}, projection={"_id": 0})

async def save_ingredient(doc): 
    """
    Save (upsert) an ingredient document into Mongo.

    Expected:
        doc contains "barcode"

    Mongo schema:
        - `_id` is set to barcode so lookups are fast and unique.

    FIX:
        In your original function `update_one(...)` was not awaited.
    """
    if not doc.get("barcode"):
        raise ValueError("Ingredient doc missing 'barcode'")
    mongo_doc = {"_id": doc["barcode"], **doc}
    ingredients_collection.update_one({"_id": mongo_doc["_id"]}, {"$set": mongo_doc}, upsert=True)

async def get_or_fetch_ingredient_dict_sync( barcode: str) -> dict: #! USED
    """
    Get ingredient from DB if cached; otherwise fetch from OFF, validate,
    compute priority, store in DB, and return the stored dict.

    """
    print("fetching")
    if barcode.startswith("custom"):
        res = await get_user_ingredient_secure(barcode)
        return res
    

    cached = await get_ingredient(barcode)
    
    if cached:
        """
        If we already have it in Mongo, return immediately.
        `cached` already has `_id` removed due to projection.
        """

        return cached
    

    """
    Otherwise:
    1) Fetch product from OFF
    2) Validate into IngredientDoc (your Pydantic model)
    3) Enrich fields you want for priority logic
    4) Compute priority
    5) Dump to dict and store
    """
    product = await off_fetch_product(barcode)
    doc_model = IngredientDoc.model_validate(product)     # your function


    doc_model.categories_tags = _norm_tags(product.get("categories_tags"))
    doc_model.pnns_groups_1 = product.get("pnns_groups_1")
    doc_model.pnns_groups_2 = product.get("pnns_groups_2")
    doc_model.nova_group    = product.get("nova_group")
    # compute on the model
    priority = doc_model.compute_priority_auto()

    # dump to dict and save
    doc = doc_model.model_dump(by_alias=False, exclude_none=True)
    doc["priority_auto"] = priority
    doc["_id"] = doc["barcode"]
    await ingredients_collection.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)

    return doc

async def doc_to_ingredient_entry(doc, priority): #! USED
    """
    Convert a stored ingredient doc into an IngredientEntry.

    IngredientEntry seems to be a lightweight object:
        - barcode
        - priority
    """    
    barcode = doc.get("barcode") or doc.get("code")
    entry = IngredientEntry(barcode=barcode, priority=priority)
    return entry

async def build_ingredient(barcode, priority, set_amount, piece_weights): #!USED
        """
        Build the runtime Ingredient object used by your app.

        Steps:
        1) Load document from DB or fetch from OFF and store
        2) Read nutrients from doc["nutrients"] (if missing, use {})
        3) Build a flat dict 'data' expected by Ingredient(...)
        4) Return Ingredient(data, priority)

        """
        doc = await get_or_fetch_ingredient_dict_sync( barcode)
        print(f"the doc {doc}")
        n = doc.get("nutrients") or doc.get("nutriments") or {}

        data = {
            "product_name": doc.get("name") or doc.get("product_name") or "Unknown",
            "barcode": doc.get("barcode") or doc.get("code") ,

            "energy_kcal":        float(n.get("energy_kcal_100g") or 0),
            "carbohydrates_100g": float(n.get("carbohydrates_100g") or 0),
            "proteins_100g":      float(n.get("proteins_100g") or 0),
            "fat_100g":           float(n.get("fat_100g") or 0),
            "saturated_fat_100g": float(n.get("saturated_fat_100g") or 0),
            "sugars_100g":        float(n.get("sugars_100g") or 0),
            "fiber_100g":         float(n.get("fiber_100g") or 0),
            "salt_100g":          float(n.get("salt_100g") or 0),
            "priority":           doc.get("priority_user" or "priority_auto"),
            "piece_weight":       float(piece_weights or 0),        # e.g. 60g egg
            "user_designated_value": float(set_amount or 0), # e.g. 150g
            }
        return Ingredient(data, data["priority"])


