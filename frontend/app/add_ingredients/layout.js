"use client";

import ThreadsBackground from "@/components/ThreadsBackground";

export default function AddIngredientsLayout({ children }) {
  return (
    <div className="relative min-h-screen">
      {/* Persistent background */}
      <div className="fixed inset-0 -z-10 pointer-events-none">
        <div className="w-full h-[600px] relative">
          <ThreadsBackground
            amplitude={1}
            distance={0}
            enableMouseInteraction
          />
        </div>
      </div>

      {/* Pages render here */}
      {children}
    </div>
  );
}
