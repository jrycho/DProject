from fastapi import APIRouter, HTTPException, Depends
from app.db_files.crud.user_db_crud import search_crud, create_user_ingredients, get_user_ingredients, get_user_key as get_user_key_crud, add_user_shared_keys as add_user_shared_keys_crud, get_user_shared_keys as get_user_shared_keys_crud, delete_user_shared_key as delete_user_shared_key_crud, delete_user_ingredient_secure
from app.db_files.crud.meal_logs_crud import ingredient_doc_to_button_json
from app.security.security import get_current_user_id
from app.db_files.models.ingredient import IngredientDoc
from app.db_files.models.ingredient_entry import IngredientEntryTemp
from uuid import uuid4
from app.db_files.crud.temp_ingredients_crud import  create_temp_meal, add_ingredient_to_temp_meal, delete_ingredient_from_temp_meal, get_temp_meal, return_temp_ingredients_button
from app.db_files.crud.user_db_crud import create_user_ingredients
from app.db_files.crud.temp_ingredients_crud import get_total_normalized_temp_nutrients, delete_all_ingredients_from_temp, set_amount_in_temp_meal    
from app.models.payload_inputs import BarcodePayload, SaveTempToPermPayload, SearchPayload, SharedKeyPayload, TempIngredientAmountPayload, TempIngredientPayload, UserIngredientPayload


router = APIRouter(prefix="/User_functions", tags=["UF"])

@router.post("/add_user_ingredient")
async def add_user_ingredient(payload: UserIngredientPayload, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        resp = await create_user_ingredients(
            user_id=user_id,
            payload=payload.model_dump(by_alias=True, exclude_none=True),
        )
        if not resp.inserted_id:
            raise HTTPException(500, "Insert failed")
        return {"message": f"User ingredient added successfully, id: {resp.inserted_id} "}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/get_user_ingrediend")
async def get_user_ingredient(name: str, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        resp = await get_user_ingredients(user_id=user_id, name=name)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#******
@router.get("/get_user_key")
async def get_user_key(user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        resp = await get_user_key_crud(user_id=user_id)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add_user_shared_id")
async def add_key_to_library(payload: SharedKeyPayload, user_id: str = Depends(get_current_user_id)):
    shared_key = payload.shared_key
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        resp = await add_user_shared_keys_crud(user_id=user_id, shared_key=shared_key)
        return {f"key '{shared_key}' succesfully added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_user_shared_keys")
async def get_user_shared_keys(user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    resp = await get_user_shared_keys_crud(user_id=user_id)
    return resp


@router.delete("/delete_user_shared_key/{shared_key}")
async def delete_user_shared_key(shared_key: str, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    await delete_user_shared_key_crud(user_id=user_id, shared_key=shared_key)
    return {"message": f"Shared key '{shared_key}' deleted"}


@router.post("/add_user_ingredient_direct")
async def add_user_ingredient_direct(payload: UserIngredientPayload, user_id:str = Depends(get_current_user_id)):

    barcode = f"custom-{user_id}-{uuid4().hex[:8]}"

    # Validate here
    validated = IngredientDoc.model_validate({
        **payload.model_dump(by_alias=True, exclude_none=True),
        "code": barcode
    })

    # Pass clean dict to CRUD
    clean_payload = validated.model_dump(by_alias=True)

    resp = await create_user_ingredients(user_id=user_id, payload=clean_payload)
    if not resp.inserted_id:
        raise HTTPException(500, "Insert failed")
    return {"message": f"User ingredient added successfully, id: {resp.inserted_id} "}





#******#******#******#******#******#******#******#******#******#******#******#******#******#******#******
@router.post("/search")
async def search(payload: SearchPayload, user_id:str=Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        resp = await search_crud(payload.query, user_id=user_id)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@router.post("/add_ingredient_to_log")
async def add_ingredient_to_temp_log(payload: TempIngredientPayload, user_id:str=Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    doc = await get_temp_meal(user_id=user_id)

    if doc is None:
        resp = await create_temp_meal( user_id = user_id)
        if resp is None:
            raise HTTPException(500, "Insert failed")
    resp = await add_ingredient_to_temp_meal(user_id=user_id, ingredient=payload)
    return resp
    
@router.post("/delete_ingredient_from_log")
async def delete_ingredient_from_temp_log(payload: BarcodePayload, user_id:str=Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    resp=await delete_ingredient_from_temp_meal(barcode=payload.barcode, user_id=user_id)
    return "Ingredient deleted successfully"



@router.post("/fetch_temp_ingredients_buttons")
async def fetch_temp_ingredients_buttons(user_id:str=Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    doc = await return_temp_ingredients_button(user_id=user_id)
    if doc is None:
        raise HTTPException(500, "failed to fetch temp ingredients buttons")
    return doc


@router.post("/save_temp_to_perm")
async def save_temp_to_perm(payload: SaveTempToPermPayload, user_id:str=Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    nutriments = await get_total_normalized_temp_nutrients(user_id=user_id)
    if nutriments is None:
        raise HTTPException(500, "Failed to get total normalized temp nutrients")
    validated_payload = UserIngredientPayload.model_validate(
        {
            **payload.model_dump(by_alias=True, exclude_none=True),
            "nutriments": nutriments,
        }
    )

    resp = await create_user_ingredients(
        payload=validated_payload.model_dump(by_alias=True, exclude_none=True),
        user_id=user_id,
    )
    if not resp.inserted_id:
        raise HTTPException(500, "Insert failed")
    await delete_all_ingredients_from_temp(user_id=user_id)
    
    return {"message": f"User ingredient added successfully, id: {resp.inserted_id} "}

@router.post("/set_amount_in_temp_")
async def set_amount_in_temp_(payload: TempIngredientAmountPayload, user_id:str=Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    resp = await set_amount_in_temp_meal(barcode=payload.barcode, amount=payload.amount, user_id=user_id)
    return "Ingredient added successfully"


@router.delete("/delete_user_ingredient/{barcode}")
async def delete_user_ingredient(barcode:str, user_id:str=Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    res = await delete_user_ingredient_secure(barcode=barcode, user_id=user_id)
    return res
    
