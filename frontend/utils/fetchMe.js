import { authFetch } from "./authFetch";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;

export async function fetchMe() {
  const res = await authFetch(`${API_ORIGIN}/Auth/me`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to fetch me: ${res.status} ${text}`);
  }

  return res.json(); // expects something like { username: "...", ... }
}
