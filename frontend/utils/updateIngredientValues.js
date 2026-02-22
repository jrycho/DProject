import { authFetch } from "./authFetch";
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;

export async function updateIngredientValues(barcode, mealId, setWeight, pieceWeight) {
  const res = await authFetch(
    `${API_ORIGIN}/logs/update_set_and_piece_weights` +
      `?barcode=${encodeURIComponent(barcode)}` +
      `&meal_id=${encodeURIComponent(mealId)}` +
      `&set_amount=${encodeURIComponent(setWeight)}` +
      `&piece_weight=${encodeURIComponent(pieceWeight)}`,
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
