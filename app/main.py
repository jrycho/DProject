import uvicorn
from fastapi import FastAPI, HTTPException
import requests
import os
from typing import List

from app.models.ingredient import Ingredient
from app.models.input_obj import InputObject
from app.models.settings import Settings, SettingsInput



from uuid import uuid4
from pydantic import BaseModel
from app.optimizers.gwo_optimizer import gwo_optimizer
from fastapi.middleware.cors import CORSMiddleware

from app import routes
from app.routes import meal_logs_routes, settings_routes, optimization_routes, testing_routes, users_routes, login_routes
from app.state.state import active_meals
import app.state.state as state






""" Global vars for meals "db" and session settings, should be both loaded from db. TODO: DO IT """
#active_meals = {}

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
Include router for meal log
"""



app.include_router(meal_logs_routes.router)
app.include_router(settings_routes.router)   
app.include_router(optimization_routes.router)
app.include_router(testing_routes.router)
app.include_router(users_routes.router)
app.include_router(login_routes.router)

"""  
Post function, create a meal, should be called on task loading
"""
@app.post("/meal")
def create_meal():
    meal_id = str(uuid4())
    active_meals[meal_id] = InputObject()
    return {"meal_id": meal_id}


    
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
    global session_sttings
    session_settings = settings_obj
    return {"message": "Settings saved"}


"""  
Get session settings returns
"""
@app.get("/session_settings")
def get_session_settings():
    if state.session_settings is None:
        raise HTTPException(status_code=404, detail="Settings not found")
    else:
        return state.session_settings.__dict__


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
    
    if state.session_settings is None:
        raise HTTPException(status_code=404, detail="Settings not found")
    
    optimization_object = gwo_optimizer(state.session_settings,active_meals[meal_id])
    optimization_object.solve()
    return optimization_object.get_json_results()


""" RUNNING ON TURN ON """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",        # "<module>:<app-instance>"
        host="0.0.0.0",     # or "127.0.0.1"
        port=8000,          # pick your port
        reload=True         # auto‑reload on code changes
    )