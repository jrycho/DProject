"use client";

import { useState } from "react";
import Navbar from "@/components/Navbar";
import { useRouter } from "next/navigation";
import { forgottenPassword } from "@/utils/forgottenPassword";
import AppBackground from "@/components/AppBackground";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

export default function ForgottenPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const router = useRouter();

  const handleForgottenPassword = async () => {
  try {
    await forgottenPassword({email: email});
    setMessage("Reset email sent successfully.");

    setTimeout(() => {
      router.push("/login");
    }, 1500);
  } catch (err) {
    setMessage("Invalid email");
  }
};

  return (
    <>
      <Navbar />

      <AppBackground />

      {/* Page spacing */}
      <div className="pt-30 px-4">
        {/* Card */}
        <div className="max-w-[520px] mx-auto p-6 bg-gray-700 border border-green-600 rounded-2xl shadow-lg text-white">
          <h2 className="text-2xl font-semibold mb-4">Forgotten Password</h2>

          <p className="text-sm text-gray-300 mb-4">
            Enter your email and we will send you a password reset link.
          </p>

          <div className="grid gap-3">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 bg-gray-800 border border-green-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />

            <button
              onClick={handleForgottenPassword}
              className="mt-2 py-2 px-4 rounded-lg bg-green-600 border border-green-600 text-white font-medium hover:bg-green-500 transition"
            >
              Send Reset Link
            </button>
          </div>

          <h3
            onClick={() => router.push("/login")}
            className="text-sm text-gray-300 mt-4 cursor-pointer"
          >
            Remembered your password?{" "}
            <span className="text-green-500 hover:underline">
              Log in here
            </span>
          </h3>

          <h3
            onClick={() => router.push("/signup")}
            className="text-sm text-gray-300 mt-2 cursor-pointer"
          >
            Not registered?{" "}
            <span className="text-green-500 hover:underline">
              Join us now here
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
