"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authFetch } from "@/utils/authFetch";

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

export default function ProtectedPage({ children }) {
  const router = useRouter();
  const [allowed, setAllowed] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function verifyToken() {
      const token = localStorage.getItem("token");

      if (!token) {
        router.push("/login");
        return;
      }

      try {
        const res = await authFetch(`${API_ORIGIN}/auth/profile`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });

        if (!res.ok) {
          localStorage.removeItem("token");
          router.push("/login");
          return;
        }

        if (!cancelled) {
          setAllowed(true);
        }
      } catch (err) {
        localStorage.removeItem("token");
        router.push("/login");
      }
    }

    verifyToken();

    return () => {
      cancelled = true;
    };
  }, [router]);

  if (!allowed) {
    return null;
  }

  return <>{children}</>;
}
