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

      <div className="pt-30">
        {/* Background */}
        <div className="fixed inset-0 -z-10 pointer-events-none" aria-hidden>
          <div className="absolute inset-0">
            <div className="w-full h-[600px] relative">
              <ThreadsBackground
                amplitude={1}
                distance={0}
                enableMouseInteraction={true}
              />
            </div>
          </div>
        </div>

        {/* Form container */}
        <div className="max-w-[420px] mx-auto mt-10 p-6 bg-gray-700 border border-green-600 rounded-2xl shadow-lg text-white">
          <h1 className="text-xl font-bold text-center mb-4">Reset password</h1>

          <form onSubmit={submit} className="grid gap-3">
            <div>
              <label className="text-sm">New password</label>
              <input
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type="password"
                required
                className="w-full px-3 py-2 mt-1 bg-gray-800 border border-green-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>

            <div>
              <label className="text-sm">Confirm password</label>
              <input
                value={password2}
                onChange={(e) => setPassword2(e.target.value)}
                type="password"
                required
                className="w-full px-3 py-2 mt-1 bg-gray-800 border border-green-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>

            <button
              disabled={loading}
              type="submit"
              className="mt-2 py-2 px-4 rounded-lg bg-green-600 border border-green-600 text-white font-medium hover:bg-green-500 transition disabled:opacity-60"
            >
              {loading ? "Resetting..." : "Reset password"}
            </button>
          </form>

          {msg && <p className="mt-4 text-sm text-gray-200">{msg}</p>}
        </div>
      </div>
    </>
  );
}
