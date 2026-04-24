"use client";
import react from "react";
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";
import { authFetch } from "./authFetch";

export async function getUserIngredientsSearch(query) {
  const q = (query ?? "").trim();
  if (!q) return [];

  const response = await authFetch(`${API_ORIGIN}/user-functions/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: q,
    }),
  });

  if (!response.ok) {
    throw new Error("Search failed");
  }

  return await response.json();
}
