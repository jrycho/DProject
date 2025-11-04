'use client'
import React, { useEffect, useState } from "react";

// ULTRA-MINIMAL: just a textarea.
// No buttons, no preview, no validation.
// Paste or type your JSON and you're done.

export default function JsonTextViewerIngredients({inputText = []}) {
  const items = Array.isArray(inputText) ? inputText : [];
  return (
    <div className="max-w-2xl overflow-hidden rounded-2xl border border-green-500 shadow bg-gray-500 mt-2">
      <table className="w-full text-sm">
        <thead className="bg-gray-600 text-white">
          <tr>
            <th className="text-left font-semibold px-4 py-2">Name</th>
            <th className="text-right font-semibold px-4 py-2">Grams</th>
          </tr>
        </thead>
        <tbody className="divide-y">
          {items.length === 0 ? (
            <tr>
              <td colSpan={2} className="px-4 py-3 text-center text-white">
                No ingredients
              </td>
            </tr>
          ) : (
            items.map(({ name, grams, barcode }, i) => (
              <tr key={barcode ?? i} className="">
                <td className="px-4 py-2 text-white">{name ?? "(unknown)"}</td>
                <td className="px-4 py-2 text-right text-white">{grams ?? 0} g</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}