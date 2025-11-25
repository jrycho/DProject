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


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://dproject-frontend.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # don't use "*" if you send credentials/cookies
    allow_credentials=True,         # True if you use cookies/session
    allow_methods=["*"],            # or ["GET","POST","OPTIONS",...]
    allow_headers=["*"],            # include "Authorization" for bearer tokens
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




""" RUNNING ON TURN ON """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",        # "<module>:<app-instance>"
        host="0.0.0.0",     # or "127.0.0.1"
        port=8000,          # pick your port
        reload=True         # auto‑reload on code changes
    )