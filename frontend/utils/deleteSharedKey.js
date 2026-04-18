import { authFetch } from "./authFetch";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

export async function deleteSharedKey(sharedKey) {
  const res = await authFetch(
    `${API_ORIGIN}/User_functions/delete_user_shared_key/${encodeURIComponent(sharedKey)}`,
    {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    },
  );

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to delete shared key: ${res.status} ${text}`);
  }

  return res.json();
}
