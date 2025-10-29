from fastapi import FastAPI, HTTPException
import requests
from app.models.ingredient import Ingredient
from app.db_files.crud.ingredient_crud import get_or_fetch_ingredient_dict_sync

#Deletable
def build_ingredient_from_barcode(barcode: str, priority: int) -> Ingredient:
    pass

async def build_ingredient_from_db(barcode: str, priority:int):
    pass