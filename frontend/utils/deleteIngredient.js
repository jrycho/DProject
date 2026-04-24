import { authFetch } from './authFetch';
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";;

export async function deleteIngredient(mealId, barcode){
      const res = await authFetch(`${API_ORIGIN}/meal-logs/${encodeURIComponent(mealId)}/ingredients?barcode=${encodeURIComponent(barcode)}`,
    {
       method: "DELETE",
      headers: {"Content-Type": "application/json",},
    }
  );
    if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Delete failed: ${res.status}`);
  }

  // Your FastAPI might return 204 or 200 with JSON:
  return res.status === 204 ? null : await res.json();

}
