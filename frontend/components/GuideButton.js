'use client';

import { useState } from 'react';
import { createPortal } from 'react-dom';
import { guideTexts } from '../utils/guideTexts';

export default function GuideButton({ guideKey, buttonText = "?" }) {
  const [isOpen, setIsOpen] = useState(false);

  const guide = guideTexts[guideKey];
  const contentParts = guide?.content?.split("<n>") ?? [];

  if (!guide) {
    return null; // Or handle error
  }

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="bg-gray-600 border border-green-600 rounded-full hover:bg-gray-500 text-white w-8 h-8 flex items-center justify-center transition-colors text-sm font-semibold"
      >
        {buttonText}
      </button>

      {isOpen && createPortal(
        <div
          className="fixed inset-0 z-[99999] flex items-center justify-center bg-black/40"
          onMouseDown={(e) => {
            if (e.target === e.currentTarget) setIsOpen(false);
          }}
        >
          <div
            className="w-[450px] rounded-xl border border-green-600 bg-gray-700 p-4 shadow-lg"
            onMouseDown={(e) => e.stopPropagation()}
          >
            <div className="text-white">
              <h2 className="text-lg font-semibold mb-3">{guide.title}</h2>
              <div className="text-sm leading-relaxed text-gray-200 space-y-3">
                {contentParts.map((part, index) => (
                  <p key={`${guideKey}-${index}`}>{part.trim()}</p>
                ))}
              </div>
            </div>
          </div>
        </div>,
        document.body
      )}
    </>
  );
}
