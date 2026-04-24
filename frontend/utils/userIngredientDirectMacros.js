"use client";
import react from "react";
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";
import { authFetch } from "./authFetch";

export async function addUserIngredientDirect(payload) {
  const res = await authFetch(
    `${API_ORIGIN}/user-functions/ingredients/direct`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    },
  );

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    // throw backend detail (FastAPI usually returns { detail: ... })
    const msg = data?.detail
      ? JSON.stringify(data.detail)
      : JSON.stringify(data ?? {});
    throw new Error(msg || `HTTP ${res.status}`);
  }

  return data;
}
