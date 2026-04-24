import { authFetch } from "./authFetch";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

export async function getSharedKeys() {
  const res = await authFetch(`${API_ORIGIN}/user-functions/shared-keys`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to fetch shared keys: ${res.status} ${text}`);
  }

  return res.json();
}
