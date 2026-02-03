import pytest
from fastapi import status
from app.utils.settingsPayload import SettingsPayload

@pytest.mark.asyncio
async def test_create_settings(client, fake_db):
    payload = {
        "optimized_properties": ["kcal", "protein", "carbs", "fat"],
        "target_goal": [600.0, 30.0, 60.0, 20.0],
        "excess_weights": [1.0, 1.0, 1.0, 1.0],
        "slack_weights": [1.0, 1.0, 1.0, 1.0],
    }
        
    resp = await client.post(f"/settings/save_settings", json= payload)
    assert resp.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_get_settings(client, fake_db):
    await fake_db.user_settings.clear()
    """ Not found in the db - raise default values"""
    resp = await client.get((f"/settings/get_settings"))
    data = resp.json()
    print(data)
    assert resp.status_code == status.HTTP_200_OK, f"{resp.status_code} - {resp.text}"
    assert data["target_goal"] ==  [300.0, 20.0, 40.0, 12.0]
    """ Found in the db - raise designated values"""
    await fake_db.user_settings.clear()
    await fake_db.user_settings.insert_one({
                                      "user_id" : "test_id",
                                      "optimized_properties": ["kcal", "protein", "carbs", "fat"],
                                      "target_goal": [460.0, 30.0, 60.0, 20.0],
                                      "excess_weights": [1.0, 1.0, 1.0, 1.0],
                                      "slack_weights": [1.0, 1.0, 1.0, 1.0], })
    resp = await client.get((f"/settings/get_settings"))
    data = resp.json()
    print(data)
    assert resp.status_code == status.HTTP_200_OK, f"{resp.status_code} - {resp.text}"
    assert data["target_goal"] ==  [460.0, 30.0, 60.0, 20.0]