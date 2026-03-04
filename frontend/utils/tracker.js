import { authFetch } from "./authFetch";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;

/**
 * POST /Tracker/estimate_user_macros
 * Backend: estimates macros from user params, saves them as user's goal, returns DB response.
 *
 * payload example:
 * {
 *   sex: "male" | "female",
 *   weight: number,      // kg
 *   height: number,      // cm
 *   age: number,         // years
 *   activity_level: "sedentary" | "lightly_active" | "moderately_active" | "very_active" | "athlete",
 *   goal: "weight_loss" | "maintain" | "weight_gain"
 * }
 */
export async function estimateUserMacros(payload) {
  const res = await authFetch(`${API_ORIGIN}/Tracker/estimate_user_macros`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload ?? {}),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to estimate user macros: ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}

/**
 * POST /Tracker/set_user_goals
 * Backend: saves custom goal dict for the user (overrides whatever is stored).
 *
 * custom_goal example:
 * {
 *   calories: number,
 *   protein: number,
 *   fat: number,
 *   carbs: number,
 *   sat_fat?: number,
 *   fiber?: number,
 *   sodium?: number,
 *   salt?: number,
 *   cholesterol?: number
 * }
 */
export async function setUserGoals(customGoal) {
  const res = await authFetch(`${API_ORIGIN}/Tracker/set_user_goals`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(customGoal ?? {}),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to set user goals: ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}

/**
 * POST /Tracker/fetch_tracker_data
 * Backend: returns stored user goals (macros) for the current user.
 * No body.
 */
export async function fetchTrackerData() {
  const res = await authFetch(`${API_ORIGIN}/Tracker/fetch_tracker_data`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}), // keep consistent with backend expecting a POST
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to fetch tracker data: ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}

/**
 * POST /Tracker/calculate_daily_macros
 * Backend: returns summed macros for all meals of the given date for current user.
 *
 * IMPORTANT NOTE:
 * Your backend snippet shows:
 *   @router.post("calculate_daily_macros")   (missing leading "/")
 * and:
 *   async def calculate_daily_macros(date: str, ...)
 *
 * In practice, FastAPI will usually expect `date` as a query param unless you change it to body.
 *
 * This client sends it as JSON body: { date: "YYYY-MM-DD" }.
 * If you keep backend as-is, you might need to call:
 *   `${API_ORIGIN}/Tracker/calculate_daily_macros?date=YYYY-MM-DD`
 * instead.
 */
export async function calculateDailyMacros(date) {
  const res = await authFetch(`${API_ORIGIN}/Tracker/calculate_daily_macros?date=${date}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to calculate daily macros: ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}

/**
 * Alternate version if your backend expects date as QUERY PARAM (likely with current signature).
 * POST /Tracker/calculate_daily_macros?date=YYYY-MM-DD
 */
export async function calculateDailyMacrosQuery(date) {
  const url = new URL(`${API_ORIGIN}/Tracker/calculate_daily_macros`);
  url.searchParams.set("date", date);

  const res = await authFetch(url.toString(), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}), // body unused; keep POST consistent
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to calculate daily macros (query): ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}