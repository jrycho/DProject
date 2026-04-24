import { authFetch } from "./authFetch";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

/**
 * POST /user-functions/ingredients/temp-ingredients
 * payload must match IngredientEntryTemp on backend (e.g., { barcode, name, ... })
 */
export async function addIngredientToTempLog(barcode, mealId) {
  const payload = {
    barcode: barcode,
    amount: 0,
  };
  const res = await authFetch(`${API_ORIGIN}/user-functions/ingredients/temp-ingredients`, {
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
 * DELETE /user-functions/ingredients/temp-ingredients?barcode=...
 */
export async function deleteIngredientFromTempLog(barcode) {
  const res = await authFetch(`${API_ORIGIN}/user-functions/ingredients/temp-ingredients?barcode=${encodeURIComponent(barcode)}`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to delete ingredient from temp log: ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}

/**
 * GET /user-functions/ingredients/temp-ingredients
 * No body. Returns list (or doc) for rendering buttons.
 */
export async function fetchTempIngredientButtons() {
  const res = await authFetch(`${API_ORIGIN}/user-functions/ingredients/temp-ingredients`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to fetch temp ingredient buttons: ${res.status} ${text}`);
  }

  return res.json();
}


/**
 * POST /user-functions/ingredients/temp-ingredients/commits
 * payload = meal metadata 
 * nutriments are added automatically on backend
 */
export async function saveTempLogToPermanent(payload) {
  const res = await authFetch(
    `${API_ORIGIN}/user-functions/ingredients/temp-ingredients/commits`,
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
 * PATCH /user-functions/ingredients/temp-ingredients/amounts
 * backend expects { barcode: "...", amount: number }
 */
export async function setAmountInTemp(barcode, amount) {
  const res = await authFetch(`${API_ORIGIN}/user-functions/ingredients/temp-ingredients/amounts`, {
    method: "PATCH",
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
