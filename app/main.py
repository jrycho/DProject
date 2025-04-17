import uvicorn
from fastapi import FastAPI, HTTPException
import requests
import os
from typing import List
from models.ingredient import Ingredient
from models.input_obj import InputObject
from models.settings import Settings
from uuid import uuid4
from pydantic import BaseModel
from optimizers.gwo_optimizer import gwo_optimizer


"""  
API_NINJAS_KEY = os.environ.get("Ninjas_API_KEY")
API_NINJAS_URL = "https://api.api-ninjas.com/v1/nutrition"

class Ingredient():
    def __init__(self, name:str, calories:int):
        self.name = name
        self.calories = calories

#test_list
test_list = []
selected_list = []

name_list = ["apple", "banana", "cherry", "date", "elderberry"]
dull_value = 20
for item in name_list:
    item = Ingredient(item, dull_value)
    test_list.append(item)
    dull_value *= 2


for i in test_list:
    print(i.name, i.calories)
"""
"""NINJAS API QUERRY 
@app.get("/item/{food_item}")
def get_item(food_item: str):
    headers = {"X-Api-Key": API_NINJAS_KEY}
    params = {"query": food_item}

    response = requests.get(API_NINJAS_URL, headers=headers, params=params)

    if response.status_code == 200:
        nutrition_info = response.json()
        if nutrition_info:
            return nutrition_info
        else:
            raise HTTPException(status_code=404, detail="Food item not found.")
    else:
        raise HTTPException(status_code=response.status_code, detail="API request failed.")
"""
active_meals = {}
session_settings = None
app = FastAPI()

OPEN_FOOD_FACTS_URL = "https://world.openfoodfacts.org/cgi/search.pl"


@app.post("/meal")
def create_meal():
    meal_id = str(uuid4())
    active_meals[meal_id] = InputObject()
    return {"meal_id": meal_id}

@app.post("/meal/{meal_id}/ingredient")
def add_ingredient_by_barcode(meal_id: str, barcode: str, priority: int):
    if meal_id not in active_meals:
        raise HTTPException(status_code=404, detail="Meal not found")

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

    ingredient = Ingredient(nutrition_data, priority)
    active_meals[meal_id].add_ingredient(ingredient)

    return {
        "message": f"Ingredient '{ingredient.get_name()}' added successfully.",
        "ingredient": ingredient.__dict__
    }
    

@app.get("/meal/{meal_id}")
def get_meal(meal_id: str):
    if meal_id not in active_meals:
        raise HTTPException(status_code=404, detail="Meal not found")
    return active_meals[meal_id].get_input_list()

@app.delete("/meal/{meal_id}/ingredient")
def remove_ingredient(meal_id: str, barcode: str):
    if meal_id not in active_meals:
        raise HTTPException(status_code=404, detail="Meal not found")

    removed = False
    for ing in active_meals[meal_id].input_list:
        if ing.barcode == barcode:
            active_meals[meal_id].input_list.remove(ing)
            removed = True
            break

    if removed:
        return {"message": f"Ingredient removed from meal {meal_id}."}
    else:
        raise HTTPException(status_code=404, detail="Ingredient not found in meal.")


class SettingsInput(BaseModel):
    optimized_properties: List[str]
    excess_weights: List[int]
    slack_weights: List[int]
    target_goal: List[float]

@app.post("/settings")
def settings_creation(input: SettingsInput):
    settings_obj = Settings(
        excess_weights=input.excess_weights,
        slack_weights=input.slack_weights,
        target_goal=input.target_goal,
        optimized_properties=input.optimized_properties
    )
    global session_settings
    session_settings= settings_obj
    return {"message": "Settings saved"}

@app.get("/session_settings")
def get_session_settings():
    return session_settings.__dict__

@app.get("/optimized_weights/{meal_id}")
def get_optimized_wights(meal_id: str):
    optimization_object = gwo_optimizer(session_settings,active_meals[meal_id])
    optimization_object.solve()
    return optimization_object.get_json_results()
    
    

""" RUNNING ON TURN ON """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",        # "<module>:<app-instance>"
        host="0.0.0.0",     # or "127.0.0.1"
        port=8000,          # pick your port
        reload=True         # auto‑reload on code changes
    )