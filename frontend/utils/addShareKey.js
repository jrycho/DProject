import { authFetch } from "./authFetch";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;

export async function addShareKey(sharedId) {
  const res = await authFetch(
    `${API_ORIGIN}/User_functions/add_user_shared_id`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ shared_key: sharedId }),
    }
  );

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(
      `Failed to add share key: ${res.status} ${text}`
    );
  }

  return true;
}
