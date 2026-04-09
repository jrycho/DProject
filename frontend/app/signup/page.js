"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import AppBackground from "@/components/AppBackground";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;

export default function SignupPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [redirect, setRedirect] = useState(false);
  const router = useRouter();


useEffect(() => {
  if (!redirect) return;

  const timer = setTimeout(() => {
    router.push("/set_up_my_account");
  }, 1000);

  return () => clearTimeout(timer);
}, [redirect, router]);

  const handleSignup = async () => {
    const res = await fetch(`${API_ORIGIN}/Signup/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    if (res.ok) {
      const data = await res.json();
      setMessage("Signup successful. You can now login.");
      localStorage.setItem("token", data.access_token);
    setRedirect(true);


    } else {
      const err = await res.json();
      setMessage(`Error: ${err.detail || "Signup failed"}`);
    }
  };

  useEffect(() => {
    console.log(
      "NEXT_PUBLIC_API_URL in browser:",
      process.env.NEXT_PUBLIC_API_URL,
    );
  }, []);

  return (
  <>
    <div className="pt-30">
      <AppBackground />

      {/* Form container */}
      <div className="max-w-[520px] mx-auto p-6 bg-gray-700 border border-green-600 rounded-2xl shadow-lg text-white">
        <h2 className="text-2xl font-semibold mb-4">Sign Up</h2>

        <div className="grid gap-3">
          <input
            className="w-full px-3 py-2 bg-gray-800 border border-green-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            className="w-full px-3 py-2 bg-gray-800 border border-green-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            className="w-full px-3 py-2 bg-gray-800 border border-green-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            onClick={handleSignup}
            className="mt-2 py-2 px-4 rounded-lg bg-green-600 border border-green-600 text-white font-medium hover:bg-green-500 transition"
          >
            Sign Up
          </button>
        </div>

        {message && (
          <p className="mt-4 text-sm text-gray-200">
            {message}
          </p>
        )}
      </div>
    </div>
  </>
);
}
