'use client';

import GraphComponent from "@/components/GraphComponent";
import Dashboard from "@/components/Dashboard";
import BarcodeScannerComponent from "@/components/BarcodeReader";
import { useState } from "react";
import Portal from "@/utils/portal"; 
import { ScanLine } from "lucide-react";
import BarcodeReaderMount from "@/components/BarcodeReaderFullMount";

export default function Page() {
  const [scanning, setScanning] = useState(false);
 const [barcode, setBarcode] = useState("")

  const handleScanning = () => {
    setScanning(prev => !prev);
  };

  return (<>
    <BarcodeReaderMount onScan={setBarcode}/>

      <div className="mt-4 text-lg">
        <strong>Barcode:</strong> {barcode || "None"}
      </div>
    </>
  );
}