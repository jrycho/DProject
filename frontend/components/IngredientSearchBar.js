'use client'
import { addIngredient } from "@/utils/ingredientAdd";
import { authFetch } from "@/utils/authFetch";
import { useEffect, useState } from "react";


export default function IngredientSearchBar({ isActive = true, mealId, onAdded}) {
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
      const res = await fetch(
        `https://world.openfoodfacts.org/cgi/search.pl?search_terms=${encodeURIComponent(
          query
        )}&search_simple=1&action=process&json=1&page_size=${full ? 20 : 5}`
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
      const res = await fetch(`https://world.openfoodfacts.org/api/v0/product/${barcode}.json`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      if (data.product) {
        setSelectedProduct(data.product); // writes product as selectedData
        setFullSearch(searchProducts._id);
        setIngredientId(data.code);
        console.log("product details on set:", data.product); // log fresh value
        console.log("product barcode:" + data.code );
        return {ok: true, product: data.product, barcode:data.code}
      } else {
        setSelectedProduct(null);
      }
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
      <div className="mt-6 w-140">
        <h2 className="text-lg font-semibold mb-2 ml-4">Search Food:</h2>
        <div className="flex items-center">
          <input
            type="text"
            placeholder="Search food..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full p-2 border ml-2 rounded-md shadow-md"
          />
          <button
            onClick={async () => {
              setFullSearch(true);
              try {
                await searchProducts(true);
              } finally {
                setFullSearch(false); // reset after full search completes
              }
            }}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            disabled={loadingSearch || !query.trim()}
          >
            Search
          </button>
        </div>

        <ul className="mt-4 space-y-2">
          {loadingSearch && <li>Searching...</li>}
          {!loadingSearch && results.length === 0 && query && (
            <li>No results found.</li>
          )}
          {results.map((product) => (
            <li
              key={product.code}
              onClick={async () =>{ const data = await fetchProductDetails(product.code)
                console.log("LOOK HERE:" + data.barcode)
                await addIngredient(data.barcode, mealId)
                setQuery("")
                onAdded?.();  
              }}
              className="border p-2 rounded cursor-pointer hover:bg-gray-100 transition"
            >
          <strong>{product.product_name || "Unnamed product"}</strong>
              <br />
              <span className="text-sm text-gray-600">
                Barcode: {product.code}
              </span>
            </li>
          ))}
        </ul>
{/*
        {loadingDetails && <div className="mt-2">Loading details…</div>}
        {selectedProduct && (
          <div className="mt-3 p-3 border rounded">
            <div className="font-semibold">
              {selectedProduct.product_name || "Product"}
            </div>
            <div className="text-sm text-gray-700">
              {selectedProduct.brands}{" "}
              {selectedProduct.quantity ? `• ${selectedProduct.quantity}` : ""}
            </div>
          </div> 
        )}*/}
      </div>
    </div>
  );
}