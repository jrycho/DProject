from fastapi import APIRouter, HTTPException, Depends
from app.db_files.crud.user_db_crud import create_user_ingredients, get_user_ingredients, get_user_key as get_user_key_crud, add_user_shared_keys as add_user_shared_keys_crud, get_user_shared_keys as get_user_shared_keys_crud
from app.security.security import get_current_user_id


router = APIRouter(prefix="/User_functions", tags=["UF"])

@router.post("/add_user_ingredient")
async def add_user_ingredient(payload: dict, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        await create_user_ingredients(user_id=user_id, payload=payload)
        return {"message": "User ingredient added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/get_user_ingrediend")
async def get_user_ingredient(name: str,user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        resp = await get_user_ingredients(user_id=user_id, name=name)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
async def get_user_ingredient(shared_key: str,user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        resp = await add_user_shared_keys_crud(user_id=user_id, shared_key=shared_key)
        return resp
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