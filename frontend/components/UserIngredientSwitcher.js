"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function IngredientModeSwitcher() {
  const pathname = usePathname();

  const isSimple = pathname === "/add_ingredients";
  const isBatch =
    pathname === "/add_ingredients/add_ingredients_total_batch";
    const isMeal = pathname === "/add_ingredients/add_ingredients_from_db"

  return (
    <div className="flex gap-2 mb-4">
      {/* Simple */}
      <Link
        href="/add_ingredients"
        className={[
          "px-4 py-2 rounded border text-sm font-medium transition",
          isSimple
            ? "bg-gray-200 text-gray-900 border-gray-300"
            : "bg-gray-700 text-gray-200 border-gray-600 hover:bg-gray-600",
        ].join(" ")}
      >
        Per 100g
      </Link>

      {/* Batch */}
      <Link
        href="/add_ingredients/add_ingredients_total_batch"
        className={[
          "px-4 py-2 rounded border text-sm font-medium transition",
          isBatch
            ? "bg-gray-200 text-gray-900 border-gray-300"
            : "bg-gray-700 text-gray-200 border-gray-600 hover:bg-gray-600",
        ].join(" ")}
      >
        Total batch
      </Link>
      
      {/* As meal */}
      <Link
        href="/add_ingredients/add_ingredients_from_db"
        className={[
          "px-4 py-2 rounded border text-sm font-medium transition",
          isMeal
            ? "bg-gray-200 text-gray-900 border-gray-300"
            : "bg-gray-700 text-gray-200 border-gray-600 hover:bg-gray-600",
        ].join(" ")}
      >
        As meal
      </Link>
    </div>
  );
}
