"use client";

import { useEffect, useId, useRef, useState } from "react";

export default function BarcodeScannerComponent({ scanning, onScan }) {
  const rawReaderId = useId();
  const readerId = rawReaderId.replace(/[:]/g, "");
  const scannerRef = useRef(null);
  const mountedRef = useRef(true);
  const [error, setError] = useState("");

  useEffect(() => {
    mountedRef.current = true;

    return () => {
      mountedRef.current = false;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function cleanupScanner() {
      const scanner = scannerRef.current;
      if (!scanner) return;

      try {
        if (scanner.isScanning) {
          await scanner.stop();
        }
      } catch (err) {
        console.error("Stop error:", err);
      }

      try {
        await scanner.clear();
      } catch (err) {
        console.error("Clear error:", err);
      }

      if (!cancelled) {
        scannerRef.current = null;
      }
    }

    async function startScanner() {
      if (!scanning) {
        await cleanupScanner();
        if (!cancelled && mountedRef.current) {
          setError("");
        }
        return;
      }

      try {
        const { Html5Qrcode } = await import("html5-qrcode");
        if (cancelled || !mountedRef.current) return;

        const target = document.getElementById(readerId);
        if (!target) {
          throw new Error("Scanner mount point is missing.");
        }

        await cleanupScanner();
        if (cancelled || !mountedRef.current) return;

        const scanner = new Html5Qrcode(readerId);
        scannerRef.current = scanner;
        setError("");

        await scanner.start(
          { facingMode: "environment" },
          {
            fps: 10,
            qrbox: { width: 220, height: 110 },
            aspectRatio: 1.7777778,
          },
          (decodedText) => {
            if (!mountedRef.current || cancelled) return;
            onScan?.(decodedText);
          },
          () => {},
        );
      } catch (err) {
        console.error("Start error:", err);
        if (!cancelled && mountedRef.current) {
          setError("Camera failed to start.");
        }
      }
    }

    void startScanner();

    return () => {
      cancelled = true;
      void cleanupScanner();
    };
  }, [readerId, scanning, onScan]);

  return (
    <div className="relative flex w-[min(92vw,320px)] flex-col items-center gap-3">
      <div className="relative flex h-[220px] w-full justify-center overflow-hidden rounded-xl border border-green-600 bg-black">
        <div id={readerId} className="h-full w-full" />

      </div>

      {error ? <p className="text-sm text-red-300">{error}</p> : null}
    </div>
  );
}
