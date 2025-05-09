from fastapi import FastAPI, HTTPException
import requests
from app.models.ingredient import Ingredient

def build_ingredient_from_barcode(barcode: str, priority: int) -> Ingredient:
    """Builds an ingredient from a barcode.

    Args:
        barcode (str): The barcode of the product.
        priority (int): The priority of the ingredient.

    Returns: Ingredient obj
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Open Food Facts API failed")

    data = response.json()
    product = data.get("product")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    nutriments = product.get("nutriments", {})

    nutrition_data = {
        "product_name": product.get("product_name", "Unknown"),
        "energy_kcal": nutriments.get("energy-kcal_100g"),
        "fat_100g": nutriments.get("fat_100g"),
        "saturated_fat_100g": nutriments.get("saturated-fat_100g"),
        "carbohydrates_100g": nutriments.get("carbohydrates_100g"),
        "sugars_100g": nutriments.get("sugars_100g"),
        "fiber_100g": nutriments.get("fiber_100g"),
        "proteins_100g": nutriments.get("proteins_100g"),
        "salt_100g": nutriments.get("salt_100g"),
        "barcode": product.get("code"),
    }

    return Ingredient(nutrition_data, priority)

