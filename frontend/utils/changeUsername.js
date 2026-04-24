import { authFetch } from "./authFetch";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

export async function changeUsername(newUsername) {
  const res = await authFetch(
    `${API_ORIGIN}/auth/profile/username?new_username=${encodeURIComponent(newUsername)}`,
    {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
    }
  );

  const text = await res.text();

  if (!res.ok) {
    // FastAPI sends: {"detail":"..."}
    let msg = "Failed to change username";

    try {
      const json = JSON.parse(text);
      msg = json.detail || msg;
    } catch {
      msg = text || msg;
    }

    throw new Error(msg);
  }

  return JSON.parse(text); // { message: "success" }
}
