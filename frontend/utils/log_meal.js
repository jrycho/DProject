import { authFetch } from '@/utils/authFetch';

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;



export async function logMeal(mealType, date) {
  const response = await authFetch(`${API_ORIGIN}/logs/log_meal?meal_type=${encodeURIComponent(mealType)}&date=${encodeURIComponent(date)}`, {
    method: "POST",
  });
  if (!response.ok) throw new Error("Failed to log meal");
  return response.json();
}