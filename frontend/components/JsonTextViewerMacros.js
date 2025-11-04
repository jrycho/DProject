'use client'
import React, { useEffect, useState } from "react";

// ULTRA-MINIMAL: just a textarea.
// No buttons, no preview, no validation.
// Paste or type your JSON and you're done.

export default function JsonTextViewerMacros({inputText = {}}) {
  const items = Object.entries(inputText)
  return (
    <div className="max-w-2xl overflow-hidden rounded-2xl border border-green-500 shadow bg-gray-500 mt-2">
      <table className="w-full text-sm">
        <thead className="bg-gray-600 text-white">
          <tr>
            <th className="text-left font-semibold px-4 py-2">Property</th>
            <th className="text-right font-semibold px-4 py-2">Value</th>
          </tr>
        </thead>
        <tbody className="divide-y">
          {items.length === 0 ? (
            <tr>
              <td colSpan={2} className="px-4 py-3 text-center text-white">No data</td>
            </tr>
          ) : (
            items.map(([prop, val]) => (
              <tr key={prop}>
                <td className="px-4 py-2 text-white">{prop}</td>
                <td className="px-4 py-2 text-right text-white">{val}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}