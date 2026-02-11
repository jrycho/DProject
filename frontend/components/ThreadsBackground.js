"use client";
import React from "react";
import Threads from "@/components/Threads";

const ThreadsBackground = React.memo(function ThreadsBackground(props) {
  return (
    <div className="fixed inset-0 -z-10 pointer-events-none">
      <div className="w-full h-[600px] relative">
        <Threads {...props} />
      </div>
    </div>
  );
});

export default ThreadsBackground;
