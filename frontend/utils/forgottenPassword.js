const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;

export async function forgottenPassword(email) {

  const res = await fetch(
    `${API_ORIGIN}/Signup/forgotten_password?email=${encodeURIComponent(email)}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    }
  );

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to request password reset: ${res.status} ${text}`);
  }

  return true;
}
