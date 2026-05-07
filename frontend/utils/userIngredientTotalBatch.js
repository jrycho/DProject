"use client";
import react from "react";
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";
import { authFetch } from "./authFetch";

/*
Builds payload for a custom ingredient entered as total batch values.
The backend expects nutrients normalized per 100g, so this converts
whole-batch nutrient totals into per-100g nutriments before sending/saving.
*/
function buildNormalizedPayload({
  name,
  priorityUser,
  totalWeightG,
  values,
  selected,
  mode = "per100g",
}) {
  const w = Number(totalWeightG);

  // Total batch weight is needed as denominator for per-100g conversion.
  if (!Number.isFinite(w) || w <= 0) {
    throw new Error("Total weight must be > 0");
  }

  // Convert selected whole-batch nutrient totals into per-100g nutriment values.
  const nutriments = selected.reduce((acc, k) => {
    const raw = values[k];
    const total = raw === "" || raw == null ? NaN : Number(raw);

    // Keep invalid optional values empty so the caller can decide how strict to be.
    if (!Number.isFinite(total) || total < 0) {
      acc[k] = "";
      return acc;
    }

    const per100 = (total / w) * 100;
    acc[k] = Number(per100.toFixed(6));
    return acc;
  }, {});

  // Shape matches the user ingredient payload expected by backend custom ingredient endpoints.
  return {
    product_name: name,
    priority: Number(priorityUser),
    nutriments,
    batch_weight_g: w,
    normalization: mode,
  };
}
