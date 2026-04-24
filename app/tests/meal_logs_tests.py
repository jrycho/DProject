import pytest
from fastapi import status, Depends
from app.security.security import get_current_user_id, get_current_user

@pytest.mark.asyncio
async def test_meal_logs_routes(client):
    payload = {"meal_type":"Lunch", "date":"2025-11-27", }
    resp = await client.post("/meal-logs", params=payload)
    print(resp.json())
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["message"] ==  "Meal logged"

@pytest.mark.asyncio
async def test_add_meal_with_id(client,fake_db):
    fake_db.meal_logs.clear()
    payload = {"meal_type":"Breakfast", "date":"2025-11-27", "meal_id":"test_meal_id", }
    resp = await client.post("/meal-logs/custom-id", params=payload)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["message"] ==  "Meal logged"




@pytest.mark.asyncio
async def test_add_ingredient_by_barcode_wrong_id(client):
    payload = {"meal_id": 1, "barcode": "1234567890", "priority": 1,}
    resp = await client.post("/meal-logs/1/ingredients/1234567890", params=payload)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

#need to be real barcode
@pytest.mark.asyncio
async def test_add_ingredient_by_barcode(client, fake_db):
    await fake_db.meal_logs.delete_many({})
    await fake_db.meal_logs.insert_one({
        "meal_id": "test_meal_id",
        "user_id": "test_id",
        "meal_type": "Breakfast",
        "date": "2025-11-27",
        "ingredients" : []
    })
    print(fake_db.meal_logs)
    payload = { "meal_id": "test_meal_id",}
    barcode = "6111035002175"
    resp = await client.post(f"/meal-logs/test_meal_id/ingredients/{barcode}", params=payload)
    assert resp.status_code == status.HTTP_200_OK, f"{resp.status_code} - {resp.text}"
    assert resp.json()["message"] ==  "Ingredient added successfully."

@pytest.mark.asyncio
async def test_delete_ingredient_by_barcode(client, fake_db):
    meal_id = "test_meal_id"
    user_id = "test_id"
    barcode = "6111035002175"

    # seed fake meal with the ingredient
    await fake_db.meal_logs.delete_many({})
    await fake_db.meal_logs.insert_one({
        "meal_id": meal_id,
        "user_id": user_id,
        "meal_type": "Breakfast",
        "date": "2025-11-27",
        "ingredients": [
            {"barcode": barcode, "name": "Test ingredient"}
        ],
    })

    resp = await client.delete(
        f"/meal-logs/{meal_id}/ingredients",
        params={"meal_id": meal_id, "barcode": barcode},  
    )
    assert resp.status_code == status.HTTP_200_OK, f"{resp.status_code} - {resp.text}"
    assert resp.json()["message"] ==   f"Ingredient {barcode} removed from meal {meal_id}"

@pytest.mark.asyncio
async def test_fetch_logs_by_date(client, fake_db):
    meal_id = "test_meal_id"
    user_id = "test_id"

    await fake_db.meal_logs.delete_many({})
    await fake_db.meal_logs.insert_one({
        "meal_id": meal_id,
        "user_id": user_id,
        "meal_type": "Breakfast",
        "date": "2025-11-27",
        "ingredients": []

    })

    resp = await client.get(f"/meal-logs/by-date", params={"date": "2025-11-27"})
    assert resp.status_code == status.HTTP_200_OK, f"{resp.status_code} - {resp.text}"

