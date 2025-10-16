import { authFetch } from './authFetch';
import { API_ORIGIN } from '@/utils/apiConfig';
const API_BASE_URL = `http://localhost:8000`;

export async function fetchIngredientButtons(mealId){
        const res = await authFetch(`${API_ORIGIN}/logs/return_ingredients_for_buttons/${encodeURIComponent(mealId)}`,
    {
      method: "GET",
      headers: {"Content-Type": "application/json",},
    }
  )
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `fetch failed: ${res.status}`);
  };
    const data = await res.json().catch(() => []);
    console.log(data)
  return Array.isArray(data) ? data : data.items ?? [];
}