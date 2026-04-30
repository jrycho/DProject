# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.db_files.core.database import get_db, db  # your real get_db
from app.security.security import get_current_user_id, get_current_user

import app.db_files.crud.ingredient_crud as ingredient_crud
import app.db_files.crud.meal_logs_crud as meal_logs_crud
import app.db_files.crud.optimization_crud as optimization_crud
import app.db_files.crud.settings_saves as settings_crud
import app.db_files.core.database as db_module  # where real db lives


from app.tests.fake_db import FakeDB
from httpx import ASGITransport 
#make fake db in pytes

def override_get_current_user():
    # return whatever your endpoints expect:
    # dict / Pydantic model / ORM model
    return {
        "user_id":"test_id",
    }

def override_get_current_user_id():
    return "test_id"


@pytest.fixture(autouse=True)
def patch_db_collections(monkeypatch, fake_db):
    # ingredients_crud.py: from app.db_files.core.database import ingredients_collection
    # -> patch the local name used in that module
    monkeypatch.setattr(
        ingredient_crud,
        "ingredients_collection",
        fake_db.ingredients_collection,      # or fake_db.ingredients
    )

    # meal_logs.py: collection = db["meal_logs"]
    monkeypatch.setattr(
        meal_logs_crud,
        "meal_logs",
        fake_db.meal_logs,
    )

    # optimization.py: from ... import optimized_macros_collection, optimized_weights_collection
    monkeypatch.setattr(
        optimization_crud,
        "optimized_macros_collection",
        fake_db.optimized_macros,
    )
    monkeypatch.setattr(
        optimization_crud,
        "optimized_weights_collection",
        fake_db.optimized_weights,
    )
    monkeypatch.setattr(
        settings_crud,
        "settings_collection",
        fake_db.user_settings,
    )

    # settings_saves.py: uses db.user_settings
    # easiest: patch the db object used there to your fake_db
    monkeypatch.setattr(settings_crud, "db", fake_db)

    # (optional) if other code imports db from core.database, patch it too:
    monkeypatch.setattr(db_module, "db", fake_db)

    yield

@pytest.fixture(autouse=True)
def use_fake_db(monkeypatch):
    fake_db = FakeDB()
    monkeypatch.setattr(db_module, "db", fake_db)
    yield

@pytest.fixture
def fake_db():
    return FakeDB()


@pytest_asyncio.fixture
async def client(fake_db):
    async def override_get_db():
        # your real get_db is sync, but FastAPI is fine with async override
        return fake_db
    #in fixture, override get_db instead get fake db
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_current_user_id] = override_get_current_user_id
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

