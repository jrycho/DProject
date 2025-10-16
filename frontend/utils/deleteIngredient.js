import { authFetch } from './authFetch';
const API_BASE_URL = `http://localhost:8000`;
import { API_ORIGIN } from '@/utils/apiConfig';
export async function deleteIngredient(mealId, barcode){
      const res = await authFetch(`${API_ORIGIN}/logs/meal/${encodeURIComponent(mealId)}/ingredient?barcode=${encodeURIComponent(barcode)}`,
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