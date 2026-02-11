from fastapi import APIRouter, HTTPException, Depends
from app.db_files.crud.user_db_crud import search_crud, create_user_ingredients, get_user_ingredients, get_user_key as get_user_key_crud, add_user_shared_keys as add_user_shared_keys_crud, get_user_shared_keys as get_user_shared_keys_crud
from app.db_files.crud.meal_logs import ingredient_doc_to_button_json
from app.security.security import get_current_user_id
from pydantic import BaseModel
from app.db_files.models.ingredient import IngredientDoc
from uuid import uuid4


router = APIRouter(prefix="/User_functions", tags=["UF"])

@router.post("/add_user_ingredient")
async def add_user_ingredient(payload: dict, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        resp = await create_user_ingredients(user_id=user_id, payload=payload)
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
async def add_key_to_library(shared_key: str,user_id: str = Depends(get_current_user_id)):
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
    try:
        resp = await get_user_shared_keys_crud(user_id=user_id)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add_user_ingredient_direct")
async def add_user_ingredient_direct(payload: dict, user_id:str = Depends(get_current_user_id)):

    barcode = f"custom-{user_id}-{uuid4().hex[:8]}"

    # Validate here
    validated = IngredientDoc.model_validate({
        **payload,
        "code": barcode
    })

    # Pass clean dict to CRUD
    clean_payload = validated.model_dump(by_alias=True)

    return await add_user_ingredient(payload=clean_payload, user_id=user_id)

#TODO: implement UI normalized



#******#******#******#******#******#******#******#******#******#******#******#******#******#******#******
@router.post("/search")
async def search(payload: dict, user_id:str=Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    query = payload.get("query")
    if query is None:
        raise HTTPException(status_code=400, detail="Missing query")
    try:
        resp = await search_crud(query, user_id=user_id)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))