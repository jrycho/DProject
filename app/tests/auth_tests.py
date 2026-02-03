import pytest
from fastapi import status

print("Signup tests started")
@pytest.mark.asyncio
async def test_signup_works(client, fake_db):
    payload = {"username":"test","email": "user@example.com", "password": "secret123"}

    resp = await client.post("/Signup/signup", json=payload)
    assert resp.status_code == status.HTTP_200_OK

    # check fake DB state
    user = await fake_db.users.find_one({"email": "user@example.com"})
    assert user is not None

    settings = await fake_db.user_settings.find_one({"user_id": user["_id"]})
    assert settings is not None

print("Signup tests ended")
print("Login tests started")

@pytest.mark.asyncio
async def test_login(client, fake_db):
    from app.db_files.crud.users import hash_password   # adjust path
    raw_password = "correctpassword"
    hashed_password = hash_password(raw_password)
    await fake_db.users.insert_one({
        "email": "user@example.com",
        "password": hashed_password,
    })
    resp = await client.post(
        "/Auth/login",
        data={"username": "user@example.com", "password": raw_password},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

print("Login tests ended")