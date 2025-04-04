
from fastapi import FastAPI, HTTPException
import requests
import os
from typing import List

print("fastAPI done")
print("import test done")

app = FastAPI()

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

app = FastAPI()

OPEN_FOOD_FACTS_URL = "https://world.openfoodfacts.org/cgi/search.pl"

@app.get("/Open_food_facts_item/{food_item}")
def get_food_data(food_item: str):
    params = {
        "search_terms": food_item,
        "search_simple": 1,
        "action": "process",
        "json": 1,
    }

    response = requests.get(OPEN_FOOD_FACTS_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        if data.get("products"):
            product = data["products"][0]  # Get the first matching product
            # Extract nutritional information
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
            }

            return nutrition_data
        else:
            raise HTTPException(status_code=404, detail="Food item not found.")

    else:
        raise HTTPException(status_code=response.status_code, detail="Open Food Facts API failed.")

@app.post("/add_items_by_name/")
def add_items_by_name(keyword:str):

    #TODO:will be replaced by sql structure
    selected_items = list(filter(lambda item: keyword in item.name, test_list))
    
    
    selected_list.extend(selected_items)
    return {"selected_items": [item.name for item in selected_list]}



@app.delete("/remove_items_by_name/")
def remove_items_by_name(keyword:str):
    global selected_list
    selected_list = list(filter(lambda item: keyword not in item.name, selected_list))
    return {"selected_items": selected_list}



@app.get("/")
def home():
    return {"message": "FastAPI is running!"}



@app.get("/get_test_list_calories")
def get_list_calories():
    value = 0
    for item in selected_list:
        value += item.calories
    return {"calories": value}


@app.get("/get_selected_list")
def get_selected_list():
    return {"selected_items": selected_list}
