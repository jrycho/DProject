"use client";

import { useEffect, useRef, useState } from "react";
import { DayPicker } from "react-day-picker";
import "react-day-picker/dist/style.css";
import Portal from "@/utils/portal";

export default function Calendar({ value, onChange }) {
  const [open, setOpen] = useState(false);
  const popupRef = useRef(null);

  useEffect(() => {
    function handleClick(e) {
      if (popupRef.current && !popupRef.current.contains(e.target)) {
        setOpen(false);
      }
    }

    if (open) {
      document.addEventListener("mousedown", handleClick);
    }

    return () => document.removeEventListener("mousedown", handleClick);
  }, [open]);

  return (
    <div>
      <button
        onClick={() => setOpen((v) => !v)}
        className="bg-gray-700 px-3 py-1 rounded hover:bg-gray-500 text-white h-8 flex items-center gap-2 transition"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path d="M7 2v2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-2V2h-2v2H9V2H7zm12 8H5v10h14V10z" />
        </svg>

        {value instanceof Date ? value.toLocaleDateString() : "Pick a date"}
      </button>

      {open && (
        <Portal>
          <div className="fixed inset-0 z-[99999] flex items-center justify-center bg-black/30">
            <div
              ref={popupRef}
              className="rounded bg-gray-500 p-4 text-white shadow-lg"
            >
              <DayPicker
                mode="single"
                required
                selected={value}
                navLayout="around"
                style={{
                  "--rdp-accent-color": "#16a34a",
                  "--rdp-accent-background-color": "rgba(22, 163, 74, 0.2)",
                  "--rdp-selected-border": "2px solid #16a34a",
                }}
                onSelect={(date) => {
                  if (!date) return;
                  onChange(date);
                  setOpen(false);
                }}
              />
            </div>
          </div>
        </Portal>
      )}
    </div>
  );
}
