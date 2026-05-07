"use client";
import { addIngredient } from "@/utils/ingredientAdd";
import { authFetch } from "@/utils/authFetch";
import { useEffect, useState } from "react";
import BarcodeReaderMount from "@/components/BarcodeReaderFullMount"

export default function IngredientSearchBar({
  isActive = true,
  mealId,
  onAdded,
  addIngredientFunction,
}) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [fullSearch, setFullSearch] = useState(false);
  const [loadingSearch, setLoadingSearch] = useState(false);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [ingredientId, setIngredientId] = useState(null);

  // if none active clear query
  useEffect(() => {
    if (!isActive) setQuery("");
  }, [isActive]);

  // clearing results when no query + debounce
  useEffect(() => {
    if (query.trim() === "") {
      setResults([]);
      return;
    }

    // skip live search while full search is active
    if (fullSearch) return;

    // searchbar timer
    const delay = setTimeout(() => {
      searchProducts(false); // live results
    }, 300);

    // when query changes, restart timeout
    return () => clearTimeout(delay);
  }, [query, fullSearch]);

  // live/full search
  const searchProducts = async (full = false) => {
    setLoadingSearch(true);
    try {
      // logging
      console.log("Searching for:", query);
      const res = await authFetch(
        `/user-functions/off_search?query=${encodeURIComponent(
          query,
        )}&page_size=${full ? 20 : 5}`,
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setResults(data.products || []);
    } catch (err) {
      console.error("Search failed:", err);
    } finally {
      setLoadingSearch(false);
    }
  };

  // fetching object from OFF function
  const fetchProductDetails = async (barcode) => {
    setLoadingDetails(true);
    try {
      setIngredientId(barcode);
      return { ok: true, barcode };
    } catch (err) {
      console.error("failed to fetch product details", err);
      setSelectedProduct(null);
    } finally {
      setLoadingDetails(false);
    }
  };

return (
  // search bar component
  <div>
    <div className="mt-6 w-full md:w-[24rem]">
      <h2 className="text-lg font-semibold mb-2 ml-4 text-white">
        Search Food:
      </h2>

      <div className="flex items-center gap-2">
        <input
          type="text"
          placeholder="Search for ingredients..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-2 ml-2 bg-gray-800 border border-green-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
        />

        <button
          onClick={async () => {
            setFullSearch(true);
            try {
              await searchProducts(true);
            } finally {
              setFullSearch(false);
            }
          }}
          className="px-4 py-2 bg-green-600 border border-green-600 text-white rounded-lg hover:bg-green-500 transition disabled:opacity-50"
          disabled={loadingSearch || !query.trim()}
        >
          Search
        </button>

        <BarcodeReaderMount onScan={setQuery} />
      </div>

      <div className="mt-4 ml-2 max-h-64 overflow-y-auto custom-scrollbar">
        <ul className="mt-4 ml-2 space-y-2">
          {loadingSearch && (
            <li className="text-gray-300">Searching...</li>
          )}

          {!loadingSearch && results.length === 0 && query && (
            <li className="text-gray-400">No results found.</li>
          )}

          {results.map((product) => (
            <li
              key={product.code}
              onClick={async () => {
                const item = await fetchProductDetails(product.code);
                console.log("LOOK HERE:" + item.barcode);

                try {
                  await addIngredientFunction(item.barcode, mealId);

                  setQuery("");
                  setResults([]);

                  onAdded?.();
                } catch (err) {
                  console.log(err);
                }

                setQuery("");
                onAdded?.();
              }}
              className="border border-green-600 bg-gray-700 p-2 rounded-lg cursor-pointer hover:bg-gray-600 transition text-white"
            >
              <strong>{product.product_name || "Unnamed product"}</strong>
              <br />

              <span className="text-sm text-gray-300">
                Barcode: {product.code}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  </div>
);
}
