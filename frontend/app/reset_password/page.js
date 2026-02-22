"use client";

import { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { resetPassword } from "@/utils/resetPassword";

import ThreadsBackground from "@/components/ThreadsBackground";
import Navbar from "@/components/Navbar";

export default function ResetPasswordPage() {
  const params = useSearchParams();
  const router = useRouter();

  const [token, setToken] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  const [msg, setMsg] = useState(null);
  const [loading, setLoading] = useState(false);

  // Get token from URL
  useEffect(() => {
    const t = params.get("token");
    if (t) setToken(t);
  }, [params]);

  async function submit(e) {
    e.preventDefault();
    setMsg(null);

    if (!token) {
      setMsg("Invalid reset link.");
      return;
    }

    if (password !== password2) {
      setMsg("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      await resetPassword(token, password);

      setMsg("Password reset successful. Redirecting...");

      // Redirect to login after success
      setTimeout(() => {
        router.push("/login");
      }, 1000);
    } catch (err) {
      setMsg(err.message || "Reset failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <ThreadsBackground />
      <Navbar />

      <div style={{ maxWidth: 420, margin: "40px auto" }}>
        <h1 className="text-xl font-bold text-center">Reset password</h1>

        <form onSubmit={submit}>
          <label>New password</label>
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            required
            style={{
              width: "100%",
              padding: 10,
              marginTop: 6,
              marginBottom: 12,
            }}
          />

          <label>Confirm password</label>
          <input
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            type="password"
            required
            style={{
              width: "100%",
              padding: 10,
              marginTop: 6,
              marginBottom: 12,
            }}
          />

          <button
            disabled={loading}
            type="submit"
            style={{ width: "100%", padding: 10 }}
          >
            {loading ? "Resetting..." : "Reset password"}
          </button>
        </form>

        {msg && <p style={{ marginTop: 12 }}>{msg}</p>}
      </div>
    </>
  );
}
