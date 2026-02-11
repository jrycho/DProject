"use client";
import react from "react";
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;
import { authFetch } from "./authFetch";

function buildNormalizedPayload({
  name,
  priorityUser,
  totalWeightG,
  values,      // { protein_100g?: "...", fat_100g?: "...", ... } OR totals you collect
  selected,    // array of keys (nutrient keys)
  mode = "per100g", // keep this
}) {
  const w = Number(totalWeightG);

  if (!Number.isFinite(w) || w <= 0) {
    throw new Error("Total weight must be > 0");
  }

  // values are assumed to be TOTALS for the whole batch in grams (or same unit)
  // We convert them to per 100g numbers for API nutriments.
  const nutriments = selected.reduce((acc, k) => {
    const raw = values[k];
    const total = raw === "" || raw == null ? NaN : Number(raw);

    if (!Number.isFinite(total) || total < 0) {
      acc[k] = ""; // or throw if you want strict
      return acc;
    }

    // normalize totals -> per 100g
    const per100 = (total / w) * 100;
    acc[k] = Number(per100.toFixed(6)); // keep decent precision
    return acc;
  }, {});

  return {
    product_name: name,
    priority: Number(priorityUser), // if backend expects it
    nutriments,
    // optional: also send meta (if your backend accepts it)
    batch_weight_g: w,
    normalization: mode,
  };
}
