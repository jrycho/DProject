"use client";

import AppBackground from "@/components/AppBackground";

export default function AddIngredientsLayout({ children }) {
  return (
    <div className="relative min-h-screen pt-10">
      <AppBackground />

      {children}
    </div>
  );
}
