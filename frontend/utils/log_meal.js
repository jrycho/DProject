import { authFetch } from '@/utils/authFetch';
import { API_ORIGIN } from '@/utils/apiConfig';
//const API_ORIGIN = 'http://localhost:8000'



export async function logMeal(mealType, date) {
  const response = await authFetch(`${API_ORIGIN}/logs/log_meal?meal_type=${encodeURIComponent(mealType)}&date=${encodeURIComponent(date)}`, {
    method: "POST",
  });
  if (!response.ok) throw new Error("Failed to log meal");
  return response.json();
}