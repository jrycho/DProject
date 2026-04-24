import { authFetch } from "./authFetch";
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

export async function optimizeFunction(mealId, mealType) {
  const url =
    `${API_ORIGIN}/meal-optimizations/${encodeURIComponent(mealId)}` +
    `?meal_type=${encodeURIComponent(mealType)}`;

  const res = await authFetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    let msg = `Request failed (${res.status})`;
    try {
      const data = await res.json();
      msg = data?.detail || data?.message || msg;
    } catch {}
    throw new Error(msg);
  }

  return res.json();
}
