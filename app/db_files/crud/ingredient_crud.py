import httpx
import os
from app.db_files.core.database import ingredients_collection
from fastapi import HTTPException
from app.db_files.models.ingredient_entry import IngredientEntry
from app.db_files.models.ingredient import IngredientDoc
from app.models.ingredient import Ingredient
from app.db_files.crud.user_db_crud import get_user_ingredient_secure

OFF_API_BASE_URL = os.getenv("OFF_API_BASE_URL", "https://world.openfoodfacts.org").rstrip("/")

"""  
Normalize Open Food Facts tag lists.
Args:
    - xs: Raw tag list from Open Food Facts.
Returns:
    - list: Lowercase tags without language prefixes.
Usage:
    - Internal helper for get_or_fetch_ingredient_dict_sync.
Workflow:
    - Treat None as empty list.
    - Keep only string values.
    - Remove prefix before ':'.
    - Lowercase tag values.
"""
def _norm_tags(xs): #! USED
    return [x.split(":")[-1].lower() for x in (xs or []) if isinstance(x, str)]


"""  
Fetch product from Open Food Facts.
Args:
    - barcode (str): Product barcode.
Returns:
    - dict: Raw Open Food Facts product object.
Usage:
    - Internal helper for get_or_fetch_ingredient_dict_sync.
Workflow:
    - Build Open Food Facts product URL.
    - Strip barcode input.
    - Fetch product with httpx async client.
    - Raise API status when Open Food Facts fails.
    - Raise 404 when product is missing.
    - Return product object.
"""
async def off_fetch_product(barcode: str) -> dict: #! USED
    barcode = str(barcode).strip()
    url = f"{OFF_API_BASE_URL}/api/v0/product/{barcode}.json"
    
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Open Food Facts API failed")

    data = response.json()
    product = data.get("product")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    return product


"""  
Search products in Open Food Facts.
Args:
    - query (str): Product search text.
    - page_size (int): Number of products to return.
Returns:
    - list: Raw Open Food Facts product objects.
Usage:
    - app/routes/user_functions_routes.py: off_search
Workflow:
    - Build Open Food Facts search URL from configured base URL.
    - Fetch products through the backend so the frontend does not call OFF directly.
    - Return products from the OFF response.
"""
async def off_search_products(query: str, page_size: int = 5) -> list[dict]: #! USED
    url = f"{OFF_API_BASE_URL}/cgi/search.pl"
    params = {
        "search_terms": query.strip(),
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": page_size,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Open Food Facts API failed")

    return response.json().get("products", [])

"""  
Get cached ingredient by barcode.
Args:
    - barcode: Ingredient barcode.
Returns:
    - dict | None: Ingredient document without MongoDB _id.
Usage:
    - Internal helper for get_or_fetch_ingredient_dict_sync.
Workflow:
    - Query ingredients collection by barcode stored as _id.
    - Exclude MongoDB _id from result.
    - Return cached document or None.
"""
async def get_ingredient(barcode):  #! USED
    return await ingredients_collection.find_one({"_id":barcode}, projection={"_id": 0})

"""  
Save ingredient document to cache.
Args:
    - doc (dict): Ingredient document containing barcode.
Returns:
    - UpdateResult: MongoDB update result.
Usage:
    - Currently no active call site found in app/.
Workflow:
    - Validate barcode is present.
    - Use barcode as MongoDB _id.
    - Upsert ingredient document into ingredients collection.
    - Return update result.
"""
async def save_ingredient(doc): 
    if not doc.get("barcode"):
        raise ValueError("Ingredient doc missing 'barcode'")
    mongo_doc = {"_id": doc["barcode"], **doc}
    res = await ingredients_collection.update_one({"_id": mongo_doc["_id"]}, {"$set": mongo_doc}, upsert=True)
    return res

"""  
Get ingredient from cache or external source.
Args:
    - barcode (str): Ingredient barcode.
Returns:
    - dict: Ingredient document.
Usage:
    - app/routes/meal_logs_routes.py: add_ingredient
    - app/db_files/crud/meal_logs_crud.py: build_input_object_from_meal_log
    - app/db_files/crud/temp_ingredients_crud.py
Workflow:
    - If barcode is custom, load user ingredient.
    - Return cached ingredient if present.
    - Fetch missing product from Open Food Facts.
    - Validate product with IngredientDoc.
    - Normalize category tags and enrichment fields.
    - Compute automatic priority.
    - Upsert ingredient into cache.
    - Return ingredient document.
"""
async def get_or_fetch_ingredient_dict_sync( barcode: str) -> dict: #! USED
    if barcode.startswith("custom"):
        res = await get_user_ingredient_secure(barcode)
        return res
    

    cached = await get_ingredient(barcode)
    
    if cached:
        return cached
    
    product = await off_fetch_product(barcode)
    doc_model = IngredientDoc.model_validate(product)


    doc_model.categories_tags = _norm_tags(product.get("categories_tags"))
    doc_model.pnns_groups_1 = product.get("pnns_groups_1")
    doc_model.pnns_groups_2 = product.get("pnns_groups_2")
    doc_model.nova_group    = product.get("nova_group")
    priority = doc_model.compute_priority_auto()

    doc = doc_model.model_dump(by_alias=False, exclude_none=True)
    doc["priority_auto"] = priority
    doc["_id"] = doc["barcode"]
    await ingredients_collection.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)

    return doc

"""  
Convert ingredient document to meal log entry.
Args:
    - doc (dict): Ingredient document.
    - priority: Priority value for the meal entry.
Returns:
    - IngredientEntry: Lightweight ingredient entry.
Usage:
    - app/routes/meal_logs_routes.py: add_ingredient
Workflow:
    - Read barcode from barcode or code field.
    - Build IngredientEntry with barcode and priority.
    - Return entry.
"""
async def doc_to_ingredient_entry(doc, priority): #! USED
    barcode = doc.get("barcode") or doc.get("code")
    entry = IngredientEntry(barcode=barcode, priority=priority)
    return entry

"""  
Build runtime Ingredient object.
Args:
    - barcode: Ingredient barcode.
    - priority: Ingredient priority.
    - set_amount: Fixed user amount.
    - piece_weights: Piece weight value.
    - min_amount: Minimum allowed amount.
    - max_amount: Maximum allowed amount.
Returns:
    - Ingredient: Runtime optimizer ingredient object.
Usage:
    - app/db_files/crud/meal_logs_crud.py: build_input_object_from_meal_log
Workflow:
    - Load ingredient from cache or fetch source.
    - Read nutrients from nutrients or nutriments field.
    - Convert required nutrient values to floats.
    - Attach optimization amount limits.
    - Return Ingredient object.
"""
async def build_ingredient(barcode, priority, set_amount, piece_weights, min_amount=0, max_amount=0): #!USED
        doc = await get_or_fetch_ingredient_dict_sync( barcode)
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
            "min_amount":         float(min_amount or 0),
            "max_amount":         float(max_amount or 0),
            }
        return Ingredient(data, priority)


