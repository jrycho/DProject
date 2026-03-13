'use client'

// React hooks
import { useEffect, useRef } from "react"

// Barcode scanning library
import { Html5Qrcode } from "html5-qrcode"

// Component receives:
// scanning → boolean (whether scanner should run)
// onScan → function to call when barcode is detected
export default function BarcodeScannerComponent({ scanning, onScan }) {

  // Stores the scanner instance so it persists between renders
  const scannerRef = useRef(null)

  useEffect(() => {

    // If scanner hasn't been created yet, create it
    if (!scannerRef.current) {
      // Html5Qrcode attaches itself to a DOM element with id="reader"
      scannerRef.current = new Html5Qrcode("reader")
    }

    // Reference to the scanner instance
    const scanner = scannerRef.current


    // Function to start the scanner
    const startScanner = async () => {

      // Only start if it's not already running
      if (!scanner.isScanning) {
        try {

          await scanner.start(
            // Use the rear camera on phones
            { facingMode: "environment" },

            // Scanner configuration
            {
              fps: 10, // how many frames per second to analyze

              // Size of the scanning area inside the camera preview
              qrbox: { width: 300, height: 200 }
            },

            // Callback when a barcode/QR code is successfully detected
            (decodedText) => {
              if (onScan) onScan(decodedText)
            },

            // Callback for scan errors (ignored here)
            () => {}
          )

        } catch (err) {
          console.error("Start error:", err)
        }
      }
    }


    // Function to stop the scanner
    const stopScanner = async () => {

      // Only stop if scanner is currently running
      if (scanner.isScanning) {
        try {
          await scanner.stop()
        } catch (err) {
          console.error("Stop error:", err)
        }
      }
    }


    // If parent component says scanning should run → start it
    if (scanning) {
      startScanner()
    } else {
      // Otherwise stop the scanner
      stopScanner()
    }

    // Cleanup when component unmounts or dependencies change
    return () => {
      stopScanner()
    }

  }, [scanning, onScan]) // Effect re-runs if scanning state or callback changes


  // Render container where the camera preview + scanner UI will appear
return (
  <div className="relative flex justify-center w-full max-w-[400px] h-[300px] mx-auto">
    
    {/* Scanner video will render here */}
    <div id="reader" className="w-full h-full" />

    {/* Frame overlay */}
    <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
      <div className="w-[220px] h-[100px] border-4 border-green-400 rounded-lg shadow-lg"></div>
    </div>

  </div>
);
}