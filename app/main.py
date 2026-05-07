import uvicorn
from fastapi import FastAPI, HTTPException
import requests
import os
from typing import List
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from app.models.ingredient import Ingredient
from app.models.input_obj import InputObject
from app.models.settings import Settings, SettingsInput

from app.db_files.core.database import unique_share_key_init

from uuid import uuid4
from pydantic import BaseModel
from app.optimizers.gwo_optimizer import gwo_optimizer
from fastapi.middleware.cors import CORSMiddleware

from app import routes
from app.routes import meal_logs_routes, settings_routes, optimization_routes, testing_routes, users_routes, login_routes, user_functions_routes, tracker_routes
from app.state.state import active_meals
import app.state.state as state
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

load_dotenv()


def _env_list(name: str, default: str) -> list[str]:
    return [
        item.strip()
        for item in os.getenv(name, default).split(",")
        if item.strip()
    ]


""" Global vars for meals "db" and session settings, should be both loaded from db. TODO: DO IT """
#active_meals = {}


#Creation of application instance
app = FastAPI(docs_url="/docs",
    openapi_url="/openapi.json",)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

CORS_ORIGINS = _env_list(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,https://dproject-frontend.onrender.com,https://jrycho.cz,https://www.jrycho.cz",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,         # True if usage cookies/session
    allow_methods=["*"],            # or ["GET","POST","OPTIONS",...]
    allow_headers=["*"],            # include "Authorization" for bearer tokens
)

OFF_API_BASE_URL = os.getenv("OFF_API_BASE_URL", "https://world.openfoodfacts.org").rstrip("/")
OPEN_FOOD_FACTS_URL = f"{OFF_API_BASE_URL}/cgi/search.pl"

"""  
Include routers
"""
app.include_router(meal_logs_routes.router)
app.include_router(settings_routes.router)   
app.include_router(optimization_routes.router)
app.include_router(testing_routes.router)
app.include_router(users_routes.router)
app.include_router(login_routes.router)
app.include_router(user_functions_routes.router)
app.include_router(tracker_routes.router)

"""
Lifeteime events
"""
@asynccontextmanager
async def lifespan():
    await unique_share_key_init()
    yield

""" RUNNING ON TURN ON """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",        # "<module>:<app-instance>"
        host="0.0.0.0",     # or "127.0.0.1"
        port=8000,          # pick port
        reload=True         # auto‑reload on code changes
    )
