const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;
export async function resetPassword(token, password) {

  const res = await fetch(
    `${API_ORIGIN}/Signup/reset_password`,
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
