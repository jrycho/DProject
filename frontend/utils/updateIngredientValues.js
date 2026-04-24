import { authFetch } from "./authFetch";
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

export async function updateIngredientValues({
  barcode,
  mealId,
  setAmount,
  pieceWeight,
  minAmount,
  maxAmount,
}) {
  const res = await authFetch(
    `${API_ORIGIN}/meal-logs/ingredient-amount-settings` +
      `?barcode=${encodeURIComponent(barcode)}` +
      `&meal_id=${encodeURIComponent(mealId)}` +
      `&set_amount=${encodeURIComponent(setAmount)}` +
      `&piece_weight=${encodeURIComponent(pieceWeight)}` +
      `&min_amount=${encodeURIComponent(minAmount)}` +
      `&max_amount=${encodeURIComponent(maxAmount)}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    }
  );

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to update ingredient: ${res.status} ${text}`);
  }

  return true;
}
