"use client";

import { useState } from "react";
import { ScanLine } from "lucide-react";
import BarcodeScannerComponent from "@/components/BarcodeReader";
import Portal from "@/utils/portal";

export default function BarcodeReaderMount({ onScan }) {
  const [scanning, setScanning] = useState(false);

  return (
    <>
      <button
        onClick={() => setScanning((prev) => !prev)}
        className="rounded bg-green-600 px-4 py-2 text-white"
      >
        <ScanLine size={16} className="h-6 w-8" />
      </button>

      {scanning ? (
        <Portal>
          <div className="fixed inset-0 z-[97] flex items-center justify-center bg-black/60 px-4">
            <div className="relative rounded-lg p-6">
              <button
                onClick={() => setScanning(false)}
                className="absolute -right-2 -top-2 flex h-8 w-8 items-center justify-center rounded-full bg-white text-black shadow-lg transition hover:bg-gray-200"
                aria-label="Close barcode scanner"
              >
                x
              </button>

              <BarcodeScannerComponent
                scanning={scanning}
                onScan={(code) => {
                  onScan?.(code);
                  setScanning(false);
                }}
              />
            </div>
          </div>
        </Portal>
      ) : null}
    </>
  );
}
