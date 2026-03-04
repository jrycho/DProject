from app.db_files.core.database import db
from typing import List, Dict

user_goals_collection = db["user_goals_collection"]
meal_log_collection = db["meal_logs"]
optimized_macro_collection = db["optimized_macros_collection"] 

async def save_new_user_goal(user_goal: dict, user_id: str):
    """Save new user goal in database"""
    result = await user_goals_collection.update_one(
        {"user_id": user_id}, {"$set":{"target_macros" : user_goal}}, upsert=True
    )

    return result

async def get_user_goals(user_id: str):
    """Get all user goals"""
    user_goals = await user_goals_collection.find_one({"user_id": user_id}, projection={"_id": 0}  )
    return user_goals


async def find_meal_logs_of_user_and_date(user_id: str, date: str):
    """Find meal logs of user and date"""
    print("user_id:", user_id)
    print("date:", date)
    cursor = meal_log_collection.find(
        {"user_id": user_id, "date": date}
    )
    print(await meal_log_collection.count_documents({}))
    return await cursor.to_list(length=10)

async def get_macros_from_meal_log(meal_id):
    """Return the macros stored in meal_log.results for the given meal_id."""
    doc = await optimized_macro_collection.find_one(
        {"meal_id": meal_id},
        projection={"_id": 0, "results": 1}
    )
    if not doc:
        return None
    return doc.get("results")


async def sum_macros_from_meals(ids_list: List[str]) -> Dict[str, float]:
    """
    Sum macros from multiple meal_ids.
    Returns dict like: {"calories": 500, "protein": 40, ...}
    """
    if not ids_list:
        return {}
    cursor = optimized_macro_collection.find(
        {"meal_id": {"$in": ids_list}},
        projection={"_id": 0, "results": 1}
    )

    docs = await cursor.to_list(length=None)

    totals: Dict[str, float] = {}

    for doc in docs:
        results = doc.get("results", {})

        for key, value in results.items():
            if isinstance(value, (int, float)):
                totals[key] = totals.get(key, 0) + value

    return totals