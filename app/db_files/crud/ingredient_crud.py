import requests
from app.db_files.core.database import ingredients_collection
from fastapi import HTTPException
from app.db_files.models.ingredient_entry import IngredientEntry
from app.db_files.models.ingredient import IngredientDoc
from app.models.ingredient import Ingredient

def _norm_tags(xs): #! USED
    return [x.split(":")[-1].lower() for x in (xs or []) if isinstance(x, str)]


async def off_fetch_product(barcode: str) -> dict: #! USED
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


    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    return product

async def get_ingredient(barcode):  #! USED
    return await ingredients_collection.find_one({"_id":barcode}, projection={"_id": 0})

async def save_ingredient(doc): 
    if not doc.get("barcode"):
        raise ValueError("Ingredient doc missing 'barcode'")
    mongo_doc = {"_id": doc["barcode"], **doc}
    ingredients_collection.update_one({"_id": mongo_doc["_id"]}, {"$set": mongo_doc}, upsert=True)

async def get_or_fetch_ingredient_dict_sync( barcode: str) -> dict: #! USED
    cached = await get_ingredient(barcode)
    if cached:
        flat = cached
        return flat
    


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
    # save to Mongo
    doc["_id"] = doc["barcode"]
    await ingredients_collection.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)
    return doc

async def doc_to_ingredient_entry(doc, priority): #! USED
    entry = IngredientEntry(barcode=doc["barcode"], priority=priority)
    return entry

async def build_ingredient(barcode, priority): #!USED
        doc = await get_or_fetch_ingredient_dict_sync( barcode)
        print(f"the doc {doc}")
        n = doc.get("nutrients") or {}

        data = {
            "product_name": doc.get("name") or "Unknown",
            "barcode": doc.get("barcode"),

            "energy_kcal":        float(n.get("energy_kcal_100g") or 0),
            "carbohydrates_100g": float(n.get("carbohydrates_100g") or 0),
            "proteins_100g":      float(n.get("proteins_100g") or 0),
            "fat_100g":           float(n.get("fat_100g") or 0),
            "saturated_fat_100g": float(n.get("saturated_fat_100g") or 0),
            "sugars_100g":        float(n.get("sugars_100g") or 0),
            "fiber_100g":         float(n.get("fiber_100g") or 0),
            "salt_100g":          float(n.get("salt_100g") or 0),
            "priority":           doc.get("priority_auto")
            }
        return Ingredient(data, data["priority"])

