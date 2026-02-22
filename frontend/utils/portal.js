import { useEffect, useState } from "react";
import { createPortal } from "react-dom";

/**
 * Portal renders children into document.body
 * instead of inside the current component tree.
 *
 * This avoids layout / transform / overflow issues.
 */
export default function Portal({ children }) {
  const [mounted, setMounted] = useState(false);

  // Wait until client-side mount (important for Next.js)
  useEffect(() => {
    setMounted(true);
  }, []);

  // Prevent SSR hydration mismatch
  if (!mounted) return null;

  // Render into <body>
  return createPortal(children, document.body);
}
