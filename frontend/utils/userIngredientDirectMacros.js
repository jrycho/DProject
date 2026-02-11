"use client";
import react from "react";
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;
import { authFetch } from "./authFetch";

export async function addUserIngredientDirect(payload) {
  const res = await authFetch(
    `${API_ORIGIN}/User_functions/add_user_ingredient_direct`,
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
