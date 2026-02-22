import { authFetch } from "./authFetch";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;

/**
 * POST /User_functions/add_ingredient_to_log
 * payload must match IngredientEntryTemp on backend (e.g., { barcode, name, ... })
 */
export async function addIngredientToTempLog(barcode, mealId) {
  const payload = {
    barcode: barcode,
    amount: 0,
  };
  const res = await authFetch(`${API_ORIGIN}/User_functions/add_ingredient_to_log`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload ?? {}),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to add ingredient to temp log: ${res.status} ${text}`);
  }

  // Backend returns resp. If it ever returns plain text, fallback gracefully.
  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}

/**
 * POST /User_functions/delete_ingredient_from_log
 * backend expects { barcode: "..." }
 */
export async function deleteIngredientFromTempLog(barcode) {
  const res = await authFetch(`${API_ORIGIN}/User_functions/delete_ingredient_from_log`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ barcode }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to delete ingredient from temp log: ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}

/**
 * POST /User_functions/fetch_temp_ingredients_buttons
 * No body. Returns list (or doc) for rendering buttons.
 */
export async function fetchTempIngredientButtons() {
  const res = await authFetch(`${API_ORIGIN}/User_functions/fetch_temp_ingredients_buttons`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to fetch temp ingredient buttons: ${res.status} ${text}`);
  }

  return res.json();
}


/**
 * POST /User_functions/save_temp_to_perm
 * payload = meal metadata 
 * nutriments are added automatically on backend
 */
export async function saveTempLogToPermanent(payload) {
  const res = await authFetch(
    `${API_ORIGIN}/User_functions/save_temp_to_perm`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload ?? {}),
    }
  );

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(
      `Failed to save temp log to permanent DB: ${res.status} ${text}`
    );
  }

  return res.json();
}


/**
 * POST /User_functions/set_amount_in_temp_
 * backend expects { barcode: "...", amount: number }
 */
export async function setAmountInTemp(barcode, amount) {
  const res = await authFetch(`${API_ORIGIN}/User_functions/set_amount_in_temp_`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ barcode, amount }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to set amount in temp: ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}