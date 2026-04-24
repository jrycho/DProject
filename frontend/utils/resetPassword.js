const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";
export async function resetPassword(token, password) {

  const res = await fetch(
    `${API_ORIGIN}/users/password-resets`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token, password }),
    }
  );

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to reset password: ${res.status} ${text}`);
  }

  return true;
}
