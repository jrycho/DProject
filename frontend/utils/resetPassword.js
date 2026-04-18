const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";
export async function resetPassword(token, password) {

  const res = await fetch(
    `${API_ORIGIN}/Signup/reset_password?token=${encodeURIComponent(token)}&password=${encodeURIComponent(password)}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    }
  );

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to reset password: ${res.status} ${text}`);
  }

  return true;
}
