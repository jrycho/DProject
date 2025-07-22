from fastapi import APIRouter, HTTPException, Depends
from app.db_files.crud.meal_logs import create_meal_log, get_all_meal_logs, add_ingredient_to_log, delete_ingredient_from_meal_log
from app.utils.build_ingredient_from_barcode import build_ingredient_from_barcode
from app.db_files.core.database import db
from app.models.input_obj import InputObject
from app.db_files.models.users import User
from app.state.state import active_meals
from app.db_files.models.ingredient_entry import IngredientEntry
from anyio.to_thread import run_sync
from uuid import uuid4
from app.security.security import get_current_user_id


router = APIRouter(prefix="/logs", tags=["Meal Logs"])

@router.post("/{meal_id}")
async def log_meal_with_id(meal_id: str): 
    """
    Log a meal by its ID.
    Calls create_meal_log function from crud.py
    returns a message and the log_id
    """

    try:
        
        log_id = await create_meal_log(meal_id)
        return {"message": "Meal logged", "log_id": log_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/")
async def log_meal(user_id: str = Depends(get_current_user_id)):
    
    """
    Log a meal creates ID.
    Calls create_meal_log function from crud.py
    returns a message and the log_id
    """

    """
    Logs a meal and returns meal and log ID.
    """
    try:
        meal_id = str(uuid4())
        user_id = str(user_id)

        log_id = await create_meal_log(meal_id=meal_id, user_id=user_id)
        return {
            "message": "Meal logged",
            "log_id": log_id,
            "meal_id": meal_id,
            "user_id": user_id  # optional, useful for debugging
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/")
async def read_logs():
    """  
    Returns all meal logs
    """
    return await get_all_meal_logs()


"""  
Post function, add an ingredient to a meal, should be called on ingredient loading
The barcode should be obtained in frontend via search
args:
meal_id: str
barcode: int - should be in form without (EAN etc...)
priority: int

Checks if in state, if not there pull from db, if not in db HTTP exception
"""

@router.post("/meal/{meal_id}/ingredient")
async def add_ingredient_by_barcode(meal_id: str, barcode: str, priority: int):
    #1 Check state, In state aditions for current work
    if meal_id not in active_meals:
        meal_doc = await db.meal_logs.find_one({"meal_id": meal_id})
        if not meal_doc:
            raise HTTPException(status_code=404, detail="Meal not found")
        
        #get ingredient doc
        #list of barcode priority objects
        active_meals[meal_id] = InputObject() #makes State object
        if meal_doc:
            for entry in meal_doc.get("ingredients", []): #iters from db ingredients
                ingr_barcode = entry["barcode"] #pulling barcode
                ingr_priority = entry["priority"] #pulling priority
                ingredient_to_add = await run_sync(build_ingredient_from_barcode, ingr_barcode, ingr_priority) #calls building function in sync
                active_meals[meal_id].add_ingredient(ingredient_to_add) #calls method, builds in state

    #2 builds ingredient in sync
    ingredient = await run_sync(build_ingredient_from_barcode, barcode, priority)
    
    #3 duplicate check, if not
    if ingredient not in active_meals[meal_id].get_input_list():
        active_meals[meal_id].add_ingredient(ingredient) #add to state

        #add to db
        log = await db.meal_logs.find_one({"meal_id": meal_id}) #finds DB log
        log_id = str(log["_id"]) #strings ID
        entry = IngredientEntry(barcode=barcode, priority=priority) #makes insertion object
        await add_ingredient_to_log(log_id, entry) #adds it to DB via crud

        print(active_meals[meal_id].get_input_list()) #console print

        return {
            "message": f"Ingredient '{ingredient.get_name()}' added successfully.",
            "ingredient": ingredient.__dict__
        }
    else:
        raise HTTPException(status_code=400, detail="Ingredient already exists in the meal.")
    
"""  
Remove ingredient by barcode
args: meal_id, barcode
Returns: message

calls crud function to remove ingredient from log
removes ingredient if in state
"""
@router.delete("/meal/{meal_id}/ingredient")
async def remove_ingredient_by_barcode(meal_id: str, barcode: str):
    await delete_ingredient_from_meal_log(meal_id, barcode)

    if meal_id in active_meals:
        input_object = active_meals[meal_id]
        input_object.remove_ingredient_by_barcode(barcode)

