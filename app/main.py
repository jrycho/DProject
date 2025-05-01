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
from fastapi.middleware.cors import CORSMiddleware




class SettingsInput(BaseModel):
    optimized_properties: List[str]
    excess_weights: List[int]
    slack_weights: List[int]
    target_goal: List[float]

""" Global vars for meals "db" and session settings, should be both loaded from db. TODO: DO IT """
active_meals = {}
session_settings = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

OPEN_FOOD_FACTS_URL = "https://world.openfoodfacts.org/cgi/search.pl"

"""  
Post function, create a meal, should be called on task loading
"""
@app.post("/meal")
def create_meal():
    meal_id = str(uuid4())
    active_meals[meal_id] = InputObject()
    return {"meal_id": meal_id}

"""  
Post function, add an ingredient to a meal, should be called on ingredient loading¨
The barcode should be obtained in frontend via search
args:
meal_id: str
barcode: int - should be in form without (EAN etc...)
priority: int
"""

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
    if ingredient not in active_meals[meal_id].get_input_list():
        active_meals[meal_id].add_ingredient(ingredient)
        print(active_meals[meal_id].get_input_list())

        return {
            "message": f"Ingredient '{ingredient.get_name()}' added successfully.",
            "ingredient": ingredient.__dict__
        }
    else:
        raise HTTPException(status_code=400, detail="Ingredient already exists in the meal.")
    
"""  
Get all active meals on execution
"""
@app.get("/meal/{meal_id}")
def get_meal(meal_id: str):
    if meal_id not in active_meals:
        raise HTTPException(status_code=404, detail="Meal not found")
    return active_meals[meal_id].get_input_list()


"""   
Delete ingredient from meal on execution
"""
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

"""  
Settings loading - TODO: handle from frontend
1. pick properties to optimize
2. That loads list in len(optimized_properties) length
3. create a list of lists with values for each property (E,S,Target)

"""


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


"""  
Get session settings returns
"""
@app.get("/session_settings")
def get_session_settings():
    if session_settings is None:
        raise HTTPException(status_code=404, detail="Settings not found")
    else:
        return session_settings.__dict__


"""  
Method for getting optimized weights for a meal, should be called on task loading
Args:
    meal_id: str - id of the meal to optimize

With check for if meal exists and if settings were loaded
"""
@app.get("/optimized_weights/{meal_id}")
def get_optimized_wights(meal_id: str):
    if meal_id not in active_meals:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    if session_settings is None:
        raise HTTPException(status_code=404, detail="Settings not found")
    
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