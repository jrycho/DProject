// optimizeApi.js
import { authFetch } from "./authFetch";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

/**
 * GET /meal-optimizations/{meal_id}/macros
 * Backend: returns optimization macros for a meal for the current user.
 */
export async function getOptimizationMacros(mealId) {
  if (mealId === undefined || mealId === null || mealId === "") {
    throw new Error("mealId is required");
  }

  const res = await authFetch(
    `${API_ORIGIN}/meal-optimizations/${encodeURIComponent(mealId)}/macros`,
    { method: "GET" }
  );

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to get optimization macros: ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}

/**
 * GET /meal-optimizations/{meal_id}/weights
 * Backend: returns optimization weights for a meal for the current user.
 */
export async function getOptimizationWeights(mealId) {
  if (mealId === undefined || mealId === null || mealId === "") {
    throw new Error("mealId is required");
  }

  const res = await authFetch(
    `${API_ORIGIN}/meal-optimizations/${encodeURIComponent(mealId)}/weights`,
    { method: "GET" }
  );

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to get optimization weights: ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}

/**
 * GET /meal-optimizations/{meal_id}/results
 * Backend: returns optimization macros and weights for a meal for the current user in shape of JSON tables form.
 */
export async function getOptimizationWeightsAndMacros(mealId) {
  if (mealId === undefined || mealId === null || mealId === "") {
    throw new Error("mealId is required");
  }

  const res = await authFetch(
    `${API_ORIGIN}/meal-optimizations/${encodeURIComponent(mealId)}/results`,
    { method: "GET" }
  );

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to get optimization weights: ${res.status} ${text}`);
  }

  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : res.text();
}
