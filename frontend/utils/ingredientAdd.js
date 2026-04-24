import React from 'react'
import { authFetch } from './authFetch';

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

export async function addIngredient(barcode, mealId) {

  const res = await authFetch( `${API_ORIGIN}/meal-logs/${encodeURIComponent(mealId)}/ingredients/${encodeURIComponent(barcode)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to add ingredient: ${res.status} ${text}`);
  }

  return true;
}

