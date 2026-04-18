"use client";

import { useState } from "react";
import Navbar from "@/components/Navbar";
import { useRouter } from "next/navigation";
import AppBackground from "@/components/AppBackground";
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const router = useRouter();

  const handleLogin = async () => {
    try {
      console.log("clicked")
      const body = new URLSearchParams();
      body.append("grant_type", "password");
      body.append("username", email);
      body.append("password", password);

      const response = await fetch(`${API_ORIGIN}/Auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: body.toString(),
      });

    if (!response.ok) {
      let errorText = "Login failed";

      if (response.status === 401) {
        errorText = "Invalid email or password.";
      } else if (response.status === 429) {
        errorText = "Too many login attempts. Please try again later.";
      } else {
        try {
          const err = await response.json();
          if (Array.isArray(err.detail)) {
            errorText = err.detail.map((e) => e.msg).join(", ");
          } else if (typeof err.detail === "string") {
            errorText = err.detail;
          } else if (typeof err.error === "string") {
            errorText = err.error;
          }
        } catch {
          errorText = `Login failed (${response.status})`;
        }
      }

      setMessage(`Error: ${errorText}`);
      return;
    }

      const data = await response.json();
      localStorage.setItem("token", data.access_token);
      setMessage("Login successful! Redirecting...");
      router.push("/home");
    } catch (error) {
      setMessage("Login failed. Check your connection or credentials.");
    }
  };

  return (
  <>
    <Navbar />

    <AppBackground />

    {/* Page spacing */}
    <div className="pt-30 px-4">

      {/* Login Card */}
      <div className="max-w-[520] mx-auto p-6 bg-gray-700 border border-green-600 rounded-2xl shadow-lg text-white">
        <h2 className="text-2xl font-semibold mb-4">Log In</h2>

        <div className="grid gap-3">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-green-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-green-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          />

          <button
            onClick={handleLogin}
            className="mt-2 py-2 px-4 rounded-lg bg-green-600 border border-green-600 text-white font-medium hover:bg-green-500 transition"
          >
            Login
          </button>
        </div>

        <h3
          onClick={() => router.push("/signup")}
          className="text-sm text-gray-300 mt-4 cursor-pointer"
        >
          Not registered?{" "}
          <span className="text-green-500 hover:underline">
            Join us now here
          </span>
        </h3>

        <h3
          onClick={() => router.push("/forgotten_password")}
          className="text-sm text-gray-300 mt-2 cursor-pointer"
        >
          Forgotten password?{" "}
          <span className="text-green-500 hover:underline">
            Change it here
          </span>
        </h3>

        {message && (
          <p className="mt-4 text-sm text-gray-200">{message}</p>
        )}
      </div>
    </div>
  </>
);
}
