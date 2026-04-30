from typing import Dict, List, Optional

from app.db_files.core.database import db

user_goals_collection = db["user_goals_collection"]
meal_log_collection = db["meal_logs"]
optimized_macro_collection = db["optimized_macros_collection"]

"""  
Normalize a goal date string.
Args:
    - raw_date (str): Raw date value.
Returns:
    - str: Normalized YYYY-MM-DD date string.
Usage:
    - Internal helper for tracker goal history functions.
Workflow:
    - Validate date value exists.
    - Strip whitespace.
    - Keep only the first 10 characters for YYYY-MM-DD format.
"""
def _normalize_goal_date(raw_date: str) -> str:
    # The frontend sends YYYY-MM-DD, so keep goal dates as simple day strings.
    if not raw_date:
        raise ValueError("goal date is required")
    # Trim whitespace and keep only the date portion in case a longer string slips through.
    return raw_date.strip()[:10]


"""  
Sort and deduplicate date strings.
Args:
    - dates (List[str]): Raw date strings.
Returns:
    - List[str]: Normalized sorted date strings.
Usage:
    - Internal helper for _coerce_goal_history and save_new_user_goal.
Workflow:
    - Normalize every date.
    - Remove duplicates with a set.
    - Sort oldest to newest.
"""
def _sort_dates(dates: List[str]) -> List[str]:
    # Normalize every incoming date, drop duplicates with a set, then sort oldest -> newest.
    return sorted({_normalize_goal_date(item) for item in dates})


"""  
Normalize saved goal history.
Args:
    - doc (Optional[dict]): Stored user goal document.
Returns:
    - List[dict]: Clean grouped goal history.
Usage:
    - Internal helper for save_new_user_goal and get_user_goals.
Workflow:
    - Return empty list when no document exists.
    - Read grouped goal history entries.
    - Skip malformed entries.
    - Normalize and sort dates.
    - Merge entries with identical target macros.
    - Sort groups by earliest date.
"""
def _coerce_goal_history(doc: Optional[dict]) -> List[dict]:
    if not doc:
        return []

    history = []

    # Only accept the grouped history shape: one target_macros entry can own many dates.
    for entry in doc.get("goal_history", []):
        if not entry:
            continue

        # Extract the list of dates assigned to this exact macro target.
        entry_dates = entry.get("dates")
        # Copy the macro dict so later mutations do not affect the original DB document.
        target_macros = dict(entry.get("target_macros", {}))
        # Skip malformed entries that are missing either the dates list or the macro payload.
        if not entry_dates or not target_macros:
            continue

        history.append(
            {
                # Keep each entry's dates normalized and sorted as soon as we ingest them.
                "dates": _sort_dates(list(entry_dates)),
                "target_macros": target_macros,
            }
        )

    # Merge entries with identical macro targets so one target stores many dates.
    merged: Dict[tuple, List[str]] = {}
    for entry in history:
        # Tuples let us use the macro dict as a stable hashable key.
        key = tuple(sorted(entry["target_macros"].items()))
        merged.setdefault(key, [])
        # If the same target exists multiple times, combine all of its dates together.
        merged[key].extend(entry["dates"])

    normalized_history = []
    for key, dates in merged.items():
        normalized_history.append(
            {
                # Convert the tuple key back into a normal dict for storage/response use.
                "dates": _sort_dates(dates),
                "target_macros": dict(key),
            }
        )

    # Order target groups by their earliest effective date to keep the history predictable.
    normalized_history.sort(key=lambda entry: entry["dates"][0] if entry["dates"] else "")
    return normalized_history


"""  
Resolve active goal for a requested date.
Args:
    - goal_history (List[dict]): Normalized grouped goal history.
    - requested_date (str): Date to resolve.
Returns:
    - Optional[dict]: Effective goal timeline item, or None.
Usage:
    - Internal helper for save_new_user_goal and get_user_goals.
Workflow:
    - Normalize requested date.
    - Expand grouped dates into a flat timeline.
    - Sort timeline by date.
    - Select the newest goal active on or before requested date.
    - Return selected goal item.
"""
def _resolve_goal_from_history(goal_history: List[dict], requested_date: str) -> Optional[dict]:
    # Normalize the requested date so it can be compared directly with stored YYYY-MM-DD strings.
    requested_day = _normalize_goal_date(requested_date)
    dated_targets = []

    # Expand grouped dates into a timeline, then choose the most recent goal that
    # is active on or before the requested day.
    for entry in goal_history:
        for goal_date in entry.get("dates", []):
            dated_targets.append(
                {
                    # Each date becomes its own timeline point paired with the owning macro target.
                    "date": _normalize_goal_date(goal_date),
                    "target_macros": dict(entry.get("target_macros", {})),
                }
            )

    if not dated_targets:
        return None

    # Sorting the flattened timeline lets us walk forward until we pass the requested day.
    dated_targets.sort(key=lambda item: item["date"])

    # Default to the earliest known goal; this also handles requests before the first change.
    selected = dated_targets[0]
    for item in dated_targets:
        # Keep advancing while the change date is not later than the requested day.
        if item["date"] <= requested_day:
            selected = item
        else:
            # Once we pass the requested day, the previous goal remains the correct one.
            break

    return selected


"""  
Save or update a dated user goal.
Args:
    - user_goal (dict): Macro goal values.
    - user_id (str): Owner of the goal.
    - goal_date (str): Effective date for this goal.
Returns:
    - UpdateResult: MongoDB update result.
Usage:
    - app/routes/tracker_routes.py: estimate_user_macros
    - app/routes/tracker_routes.py: set_user_goals
Workflow:
    - Load existing goal history.
    - Normalize requested goal date.
    - Remove old mapping for the same date.
    - Reuse existing target group if macros match.
    - Otherwise create a new target group.
    - Save grouped history back to database.
    - Return update result.
"""
async def save_new_user_goal(user_goal: dict, user_id: str, goal_date: str):
    """Save or update a dated user goal in database."""
    # Load the current stored history for this user, if any.
    existing_doc = await user_goals_collection.find_one({"user_id": user_id})
    normalized_date = _normalize_goal_date(goal_date)
    goal_history = _coerce_goal_history(existing_doc)

    cleaned_history = []
    # A date can only belong to one target definition. Remove it first so a changed
    # goal for the same day replaces the old mapping instead of duplicating it.
    for entry in goal_history:
        # Keep every date except the one we are currently rewriting.
        remaining_dates = [item for item in entry["dates"] if _normalize_goal_date(item) != normalized_date]
        if remaining_dates:
            cleaned_history.append(
                {
                    # Preserve the target entry only if it still owns at least one date.
                    "dates": _sort_dates(remaining_dates),
                    "target_macros": dict(entry["target_macros"]),
                }
            )

    # Reuse an existing target entry when the macro set already exists.
    matched_entry = None
    for entry in cleaned_history:
        if entry["target_macros"] == user_goal:
            matched_entry = entry
            break

    if matched_entry is None:
        # Brand new macro set: create a new target group starting with this date.
        cleaned_history.append(
            {
                "dates": [normalized_date],
                "target_macros": dict(user_goal),
            }
        )
    else:
        # Existing macro set: just attach the new effective date to that group.
        matched_entry["dates"] = _sort_dates([*matched_entry["dates"], normalized_date])

    # Keep groups ordered for readability and deterministic responses.
    cleaned_history.sort(key=lambda entry: entry["dates"][0] if entry["dates"] else "")

    latest_goal = _resolve_goal_from_history(cleaned_history, "9999-12-31")
    result = await user_goals_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                # Persist only the grouped history shape in the database.
                "goal_history": cleaned_history,
            }
        },
        upsert=True,
    )

    return result


"""  
Get user goals for a requested date.
Args:
    - user_id (str): Owner of the goals.
    - requested_date (str): Date to resolve.
Returns:
    - Optional[dict]: Resolved goal data, or None.
Usage:
    - app/routes/tracker_routes.py: fetch_tracker_data
Workflow:
    - Load stored goal history.
    - Return None if user has no goals.
    - Normalize stored history.
    - Resolve the active goal for requested date.
    - Return user_id, effective date, target macros, and goal history.
"""
async def get_user_goals(user_id: str, requested_date: str):
    """Resolve user goals for the requested date from dated history."""
    # Read the user's stored goal history.
    user_goals = await user_goals_collection.find_one({"user_id": user_id}, projection={"_id": 0})
    if not user_goals:
        return None

    goal_history = _coerce_goal_history(user_goals)
    # If there are gaps between two changes, the earlier goal remains active until
    # the next dated change takes over.
    resolved_goal = _resolve_goal_from_history(goal_history, requested_date)
    if not resolved_goal:
        return None

    return {
        "user_id": user_id,
        # Return the effective date that won for this request.
        "goal_date": resolved_goal["date"],
        # Return only the resolved macros the caller should use for that day.
        "target_macros": resolved_goal["target_macros"],
        # Include the normalized history so callers can inspect or debug the timeline if needed.
        "goal_history": goal_history,
    }


"""  
Find meal logs for a user and date.
Args:
    - user_id (str): Owner of the meal logs.
    - date (str): Date to match.
Returns:
    - list: Meal log documents for the date.
Usage:
    - app/routes/tracker_routes.py: calculate_daily_macros
Workflow:
    - Query meal_logs by user_id and date.
    - Convert cursor to a list.
    - Return up to 10 matching logs.
"""
async def find_meal_logs_of_user_and_date(user_id: str, date: str):
    """Find meal logs of user and date"""
    print("user_id:", user_id)
    print("date:", date)
    cursor = meal_log_collection.find({"user_id": user_id, "date": date})
    print(await meal_log_collection.count_documents({}))
    return await cursor.to_list(length=10)


"""  
Get optimized macros for one meal.
Args:
    - meal_id: Target meal ID.
Returns:
    - Optional[dict]: Optimized macro results, or None.
Usage:
    - Currently no active route imports this function.
Workflow:
    - Query optimized macros by meal_id.
    - Return None if no saved macros exist.
    - Return the results field.
"""
async def get_macros_from_meal_log(meal_id):
    """Return the macros stored in meal_log.results for the given meal_id."""
    doc = await optimized_macro_collection.find_one(
        {"meal_id": meal_id}, projection={"_id": 0, "results": 1}
    )
    if not doc:
        return None
    return doc.get("results")


"""  
Sum optimized macros from multiple meals.
Args:
    - ids_list (List[str]): Meal IDs to sum.
Returns:
    - Dict[str, float]: Summed macro totals.
Usage:
    - app/routes/tracker_routes.py: calculate_daily_macros
Workflow:
    - Return empty dict if no meal IDs are provided.
    - Query optimized macro results for all meal IDs.
    - Iterate each results dict.
    - Add numeric macro values by key.
    - Return totals.
"""
async def sum_macros_from_meals(ids_list: List[str]) -> Dict[str, float]:
    """
    Sum macros from multiple meal_ids.
    Returns dict like: {"calories": 500, "protein": 40, ...}
    """
    if not ids_list:
        return {}
    cursor = optimized_macro_collection.find(
        {"meal_id": {"$in": ids_list}}, projection={"_id": 0, "results": 1}
    )

    docs = await cursor.to_list(length=None)

    totals: Dict[str, float] = {}

    for doc in docs:
        results = doc.get("results", {})

        for key, value in results.items():
            if isinstance(value, (int, float)):
                totals[key] = totals.get(key, 0) + value

    return totals
