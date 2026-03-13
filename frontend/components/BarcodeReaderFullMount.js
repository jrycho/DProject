"use client";

import GraphComponent from "@/components/GraphComponent";
import Dashboard from "@/components/Dashboard";
import BarcodeScannerComponent from "@/components/BarcodeReader";
import { useState } from "react";
import Portal from "@/utils/portal";
import { ScanLine } from "lucide-react";

export default function BarcodeReaderMount({ onScan }) {
  const [scanning, setScanning] = useState(false);

  const handleScanning = () => {
    setScanning((prev) => !prev);
  };

  return (
    <>
      <button
        onClick={handleScanning}
        className="px-4 py-2 bg-green-600  text-white rounded"
      >
        <ScanLine size={16} className="w-8 h-6" />
      </button>

      {scanning && (
        <Portal>
          <div className="fixed inset-0  z-[97] flex items-center justify-center bg-black/60">
            <div className=" relative p-6 rounded-lg ">
              <button
                onClick={() => setScanning(false)}
                className="absolute -top-2 -right-2 w-8 h-8 flex items-center justify-center bg-white text-black rounded-full shadow-lg hover:bg-gray-200"
              >
                ✕
              </button>
              <BarcodeScannerComponent

                scanning={scanning}
                onScan={(code) => {
                  if (onScan) onScan(code); // send barcode to parent
                  setScanning(false);
                }}
              />
            </div>
          </div>
        </Portal>
      )}
    </>
  );
}
