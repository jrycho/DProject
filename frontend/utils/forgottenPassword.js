const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

export async function forgottenPassword(payload) {
  const res = await fetch(`${API_ORIGIN}/Signup/forgotten_password`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    let errorMessage = "Failed to request password reset";
    console.log("unable to request password reset");

    try {
      const err = await res.json();
      if (err.detail) errorMessage = err.detail;
    } catch {
      const text = await res.text().catch(() => "");
      if (text) errorMessage = text;
    }

    throw new Error(`${errorMessage} (${res.status})`);
  }

  return true;
}