import { authFetch } from "./authFetch";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

export async function userIngredientDelete(barcode) {
  const res = await authFetch(
    `${API_ORIGIN}/user-functions/ingredients/${barcode}`,
    {
      method: "DELETE",
    }
  );

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to delete ingredient: ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();}
