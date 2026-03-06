'use client'

import { useEffect, useRef } from "react"
import { Html5Qrcode } from "html5-qrcode"

export default function BarcodeScannerComponent({ scanning, onScan }) {
  const scannerRef = useRef(null)

  useEffect(() => {
    if (!scannerRef.current) {
      scannerRef.current = new Html5Qrcode("reader")
    }

    const scanner = scannerRef.current

    const startScanner = async () => {
      if (!scanner.isScanning) {
        try {
          await scanner.start(
            { facingMode: "environment" },
            {
              fps: 10,
              qrbox: { width: 400, height: 200 }
            },
            (decodedText) => {
              if (onScan) onScan(decodedText)
            },
            () => {}
          )
        } catch (err) {
          console.error("Start error:", err)
        }
      }
    }

    const stopScanner = async () => {
      if (scanner.isScanning) {
        try {
          await scanner.stop()
        } catch (err) {
          console.error("Stop error:", err)
        }
      }
    }

    if (scanning) {
      startScanner()
    } else {
      stopScanner()
    }

    return () => {
      stopScanner()
    }
  }, [scanning, onScan])

  return (
    <div
      id="reader"
      style={{
        width: "600px",
        maxWidth: "100%"
      }}
    />
  )
}