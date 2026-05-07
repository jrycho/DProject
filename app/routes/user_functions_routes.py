from fastapi import APIRouter, HTTPException, Depends, Query
from app.db_files.crud.user_db_crud import search_crud, create_user_ingredients, get_user_ingredients, get_user_key as get_user_key_crud, add_user_shared_keys as add_user_shared_keys_crud, get_user_shared_keys as get_user_shared_keys_crud, delete_user_shared_key as delete_user_shared_key_crud, delete_user_ingredient_secure
from app.db_files.crud.ingredient_crud import off_search_products
from app.security.security import get_current_user_id
from app.db_files.models.ingredient import IngredientDoc
from uuid import uuid4
from app.db_files.crud.temp_ingredients_crud import create_temp_meal, add_ingredient_to_temp_meal, delete_ingredient_from_temp_meal, get_temp_meal, return_temp_ingredients_button
from app.db_files.crud.temp_ingredients_crud import get_total_normalized_temp_nutrients, delete_all_ingredients_from_temp, set_amount_in_temp_meal
from app.models.payload_inputs import SaveTempToPermPayload, SearchPayload, SharedKeyPayload, TempIngredientAmountPayload, TempIngredientPayload, UserIngredientPayload


router = APIRouter(prefix="/user-functions", tags=["UF"])


#==========================================================================================
# USER INGREDIENTS ENDPOINTS
#==========================================================================================

"""  
Add a user ingredient.
This route saves a user-defined ingredient for the current user.
Args:
    - payload (UserIngredientPayload): Ingredient data.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Success message with inserted ID.
"""
@router.post("/ingredients")
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""  
Get user ingredients by name.
This route searches the current user's saved ingredients.
Args:
    - name (str): Ingredient name search value.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - list: Matching user ingredients.
"""
@router.get("/ingredients")
async def get_user_ingredient(name: str, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        resp = await get_user_ingredients(user_id=user_id, name=name)
        return resp
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""  
Add a direct user ingredient.
This route creates a custom barcode and saves validated ingredient data.
Args:
    - payload (UserIngredientPayload): Ingredient data.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Success message with inserted ID.
"""
@router.post("/ingredients/direct")
async def add_user_ingredient_direct(payload: UserIngredientPayload, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

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


"""  
Add ingredient to temporary meal log.
This route creates a temp meal if needed and adds one ingredient to it.
Args:
    - payload (TempIngredientPayload): Ingredient data for temp log.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Temp ingredient update result.
"""
@router.post("/ingredients/temp-ingredients")
async def add_ingredient_to_temp_log(payload: TempIngredientPayload, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    doc = await get_temp_meal(user_id=user_id)

    if doc is None:
        resp = await create_temp_meal(user_id=user_id)
        if resp is None:
            raise HTTPException(500, "Insert failed")
    resp = await add_ingredient_to_temp_meal(user_id=user_id, ingredient=payload)
    return resp


"""  
Delete ingredient from temporary meal log.
This route removes one ingredient from the current user's temp meal.
Args:
    - barcode (str): Ingredient barcode.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - str: Success message.
"""
@router.delete("/ingredients/temp-ingredients")
async def delete_ingredient_from_temp_log(barcode: str, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    resp = await delete_ingredient_from_temp_meal(barcode=barcode, user_id=user_id)
    return "Ingredient deleted successfully"


"""  
Fetch temporary ingredient buttons.
This route returns formatted temp ingredients for frontend buttons.
Args:
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - list: Temp ingredient button data.
"""
@router.get("/ingredients/temp-ingredients")
async def fetch_temp_ingredients_buttons(user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    doc = await return_temp_ingredients_button(user_id=user_id)
    if doc is None:
        raise HTTPException(500, "failed to fetch temp ingredients buttons")
    return doc


"""  
Save temporary ingredients as permanent ingredient.
This route normalizes temp nutrients and saves them as a user ingredient.
Args:
    - payload (SaveTempToPermPayload): Final ingredient metadata.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Success message with inserted ID.
"""
@router.post("/ingredients/temp-ingredients/commits")
async def save_temp_to_perm(payload: SaveTempToPermPayload, user_id: str = Depends(get_current_user_id)):
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


"""  
Set amount for a temporary ingredient.
This route updates amount for one ingredient in the current user's temp meal.
Args:
    - payload (TempIngredientAmountPayload): Barcode and amount.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - str: Success message.
"""
@router.patch("/ingredients/temp-ingredients/amounts")
async def set_amount_in_temp_(payload: TempIngredientAmountPayload, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    resp = await set_amount_in_temp_meal(barcode=payload.barcode, amount=payload.amount, user_id=user_id)
    return "Ingredient added successfully"


"""  
Delete a user ingredient.
This route removes one saved ingredient owned by the current user.
Args:
    - barcode (str): Ingredient barcode.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Delete result.
"""
@router.delete("/ingredients/{barcode}")
async def delete_user_ingredient(barcode: str, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    res = await delete_user_ingredient_secure(barcode=barcode, user_id=user_id)
    return res


#==========================================================================================
# SEARCH ENDPOINTS
#==========================================================================================

"""  
Search ingredients.
This route searches global and user ingredients for the current user.
Args:
    - payload (SearchPayload): Search query.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - list: Search results.
"""
@router.post("/search")
async def search(payload: SearchPayload, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        resp = await search_crud(payload.query, user_id=user_id)
        return resp
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""  
Search Open Food Facts through backend.
This route keeps Open Food Facts requests behind the API instead of the frontend.
Args:
    - query (str): Product search value.
    - page_size (int): Number of products to return.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Products returned by Open Food Facts.
"""
@router.get("/off_search")
async def off_search(
    query: str = Query(..., min_length=1),
    page_size: int = Query(5, ge=1, le=50),
    user_id: str = Depends(get_current_user_id),
):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        products = await off_search_products(query=query, page_size=page_size)
        return {"products": products}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#==========================================================================================
# SHARE KEYS ENDPOINTS
#==========================================================================================

"""  
Get personal shared key.
This route returns the current user's own sharing key.
Args:
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Personal shared key data.
"""
@router.get("/shared-keys/personal")
async def get_user_key(user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        resp = await get_user_key_crud(user_id=user_id)
        return resp
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""  
Add a shared key to library.
This route saves another user's shared key for the current user.
Args:
    - payload (SharedKeyPayload): Shared key to add.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - set: Success message.
"""
@router.post("/shared-keys")
async def add_key_to_library(payload: SharedKeyPayload, user_id: str = Depends(get_current_user_id)):
    shared_key = payload.shared_key
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        resp = await add_user_shared_keys_crud(user_id=user_id, shared_key=shared_key)
        return {f"key '{shared_key}' succesfully added"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""  
Get saved shared keys.
This route returns shared keys stored by the current user.
Args:
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - list: Saved shared keys.
"""
@router.get("/shared-keys")
async def get_user_shared_keys(user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    resp = await get_user_shared_keys_crud(user_id=user_id)
    return resp


"""  
Delete a shared key.
This route removes one shared key from the current user's library.
Args:
    - shared_key (str): Shared key to delete.
    - user_id (Depends(get_current_user_id)): Current user ID.
Returns:
    - dict: Success message.
"""
@router.delete("/shared-keys/{shared_key}")
async def delete_user_shared_key(shared_key: str, user_id: str = Depends(get_current_user_id)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    await delete_user_shared_key_crud(user_id=user_id, shared_key=shared_key)
    return {"message": f"Shared key '{shared_key}' deleted"}
