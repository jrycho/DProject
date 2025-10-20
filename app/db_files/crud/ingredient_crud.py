import requests
from app.db_files.core.database import ingredients_collection
from fastapi import HTTPException
from app.db_files.models.ingredient_entry import IngredientEntry


#copying hiphons to underscopes
def normalize_off_nutriments(n: dict) -> dict:
    if not n: 
        return {}
    n = dict(n)  # shallow copy
    if "energy-kcal_100g" in n and "energy_kcal_100g" not in n:
        n["energy_kcal_100g"] = n["energy-kcal_100g"]
    if "energy-kj_100g" in n and "energy_kj_100g" not in n:
        n["energy_kj_100g"] = n["energy-kj_100g"]
    if "energy-kcal_serving" in n and "energy_kcal_serving" not in n:
        n["energy_kcal_serving"] = n["energy-kcal_serving"]
    if "energy-kj_serving" in n and "energy_kj_serving" not in n:
        n["energy_kj_serving"] = n["energy-kj_serving"]
    return n



async def off_to_ingredient_dict(barcode: str) -> dict:
    """
    Fetch a product from OFF and return a dict with keys your Ingredient class expects.
    Raises LookupError if the barcode isn't found.
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Open Food Facts API failed")

    data = response.json()
    product = data.get("product")
    print("look here:")
    print(data)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    product = data["product"]
    nutriments = product.get("nutriments") or {}

    # Normalize common alternate keys
    kcal_100g = nutriments.get("energy-kcal_100g", nutriments.get("energy_kcal_100g"))
    sat_fat_100g = nutriments.get("saturated-fat_100g", nutriments.get("saturated_fat_100g"))

    return {
        "product_name": product.get("product_name", "Unknown"),
        "barcode": product.get("code"),
        "energy_kcal": float(kcal_100g or 0.0),

        "carbohydrates_100g": float(nutriments.get("carbohydrates_100g") or 0.0),
        "proteins_100g":      float(nutriments.get("proteins_100g") or 0.0),
        "fat_100g":           float(nutriments.get("fat_100g") or 0.0),
        "saturated_fat_100g": float(sat_fat_100g or 0.0),
        "sugars_100g":        float(nutriments.get("sugars_100g") or 0.0),
        "fiber_100g":         float(nutriments.get("fiber_100g") or 0.0),
        "salt_100g":          float(nutriments.get("salt_100g") or 0.0),
    }

async def get_ingredient(barcode):  #! USED
    return await ingredients_collection.find_one({"_id":barcode}, projection={"_id": 0})

async def save_ingredient(doc): #! USED
    if not doc.get("barcode"):
        raise ValueError("Ingredient doc missing 'barcode'")
    mongo_doc = {"_id": doc["barcode"], **doc}
    ingredients_collection.update_one({"_id": mongo_doc["_id"]}, {"$set": mongo_doc}, upsert=True)

async def get_or_fetch_ingredient_dict_sync( barcode: str) -> dict: #! USED
    doc = await get_ingredient(barcode)
    if doc:
        return doc
    doc = await off_to_ingredient_dict(barcode)   # your function
    await save_ingredient(doc)
    return doc

async def doc_to_ingredient_entry(doc, priority): #! USED
    entry = IngredientEntry(barcode=doc["barcode"], priority=priority)
    return entry
