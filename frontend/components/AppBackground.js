"use client";

import ThreadsBackground from "@/components/ThreadsBackground";

export default function AppBackground() {
  return (
    <div className="fixed inset-0 -z-10 pointer-events-none" aria-hidden>
      <div className="absolute inset-0 md:hidden bg-gradient-to-b from-black via-[#011505] to-[#035811]" />

      <div className="absolute inset-0 hidden md:block">
        <div style={{ width: "100%", height: "600px", position: "relative" }}>
          <ThreadsBackground
            amplitude={1}
            distance={0}
            enableMouseInteraction={true}
          />
        </div>
      </div>
    </div>
  );
}
