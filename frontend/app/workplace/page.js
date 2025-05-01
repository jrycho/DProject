  'use client';

  import { useEffect, useState } from 'react';
  import SettingsPanel from './settingspanel';

  const MealCreator = () => {
    const [mealId, setMealId] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const [query, setQuery] = useState('')
    const [results, setResults] = useState([])
    const [loadingSearch, setLoadingSearch] = useState(false)
    const [queryLast, setQueryLast] = useState('')
    const [fullSearch, setFullSearch] = useState(false)

    const [selectedProduct, setSelectedProduct] = useState(null)
    const [loadingDetails, setLoadingDetails] = useState(false)

    const [mealShow, setMealShow] = useState(null)
    const [showSettings, setShowSettings] = useState(false)

    
    useEffect(() => {
      if (query.trim() === '') {
        setResults([])
        return
      }
    
      const delay = setTimeout(() => {
        if (!fullSearch) {
          searchProducts(false) // live results
        }
      }, 300)
    
      return () => clearTimeout(delay)
    }, [query])
  

    const handleCreateMeal = async () => {
      setLoading(true)
      setError(null)

      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/meal`, {
          method: 'POST',
        })
        if (!res.ok) throw new Error('API error')
        const data = await res.json()
        setMealId(data.meal_id)
      } catch (err) {
        setError('Failed to create meal.')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    const searchProducts = async (full = false) => {
      setLoadingSearch(true)

      try {
        const pageSize = full ? 20 : 5
        console.log('Searching for:', query)  
        const res = await fetch(`https://world.openfoodfacts.org/cgi/search.pl?search_terms=${encodeURIComponent(query)}&search_simple=1&action=process&json=1&page_size=5`
        )
        const data = await res.json()
        setResults(data.products || [])
      } catch (err) {
        console.error('Search failed:', err)
      } finally {
        setLoadingSearch(false)
      }
      }


  const fetchProductDetails = async (barcode) => {
    setLoadingDetails(true)
    try {
      const res = await fetch(`https://world.openfoodfacts.org/api/v0/product/${barcode}.json`)
      const data = await res.json()
      if (data.product){
        setSelectedProduct(data.product)
        console.log('product details on set:', selectedProduct)
      }
      else {setSelectedProduct(null)}
    }
      catch (err) {
      console.error('failed to fetch product details', err)
      setSelectedProduct(null)}
      
        finally {setLoadingDetails(false)}
  }


  const addItemToMeal = async (mealId, barcode, priority) => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/meal/${mealId}/ingredient?barcode=${barcode}&priority=${priority}`,
      {method: 'POST'})
      const data = await res.json()
      if (res.ok) {
        console.log('adding to meal:', data)
        await showMeal(mealId)
      } else {console.log('failed to add to meal')

      }
    }
    catch (err) {console.log('failed to add to meal', err)}
  }

  const showMeal = async (mealId) => {
    if (!mealId !== null) {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/meal/${mealId}`,
        {method: 'GET'}
      )
      const data = await res.json()
      setMealShow(data)
    } else {
      console.log('mealId is null')
    }
  }


  return (
    <>
      <div className="p-4 rounded-lg shadow-md bg-black max-w-md mx-auto">
        <button
          onClick={handleCreateMeal}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Creating Meal...' : 'Create New Meal'}
        </button>

        {error && <p className="text-red-500 mt-2">{error}</p>}
        {mealId && (
          <p className="mt-4 text-green-600 font-semibold">
            Meal created! Meal ID: {mealId}
          </p>
        )}
      </div>

{/* Search bar */}


    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-2">Search Food:</h2>
      <div className="flex items-center">
        <input type="text"
        placeholder="Search food..."
        value={query}
        onChange={e => setQuery(e.target.value)}
        className="w-full p-2 border rounded-md shadow-md"/>
        <button
        onClick={() => {
        setFullSearch(true)
        searchProducts(true)
      }}
      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
>
  Search
</button>
      </div>
      

{/* Search results */}


  <ul className="mt-4 space-y-2">
  {loadingSearch && <li>Searching...</li>}
  {!loadingSearch && results.length === 0 && query && (
    <li>No results found.</li>
  )}
  {results.map((product) => (
    <li
      key={product.code}
      onClick={() => fetchProductDetails(product.code)}
      className="border p-2 rounded cursor-pointer hover:bg-gray-100 transition"
    >

      <strong>{product.product_name || 'Unnamed product'}</strong>
      <br />
      <span className="text-sm text-gray-600">Barcode: {product.code}</span>
    </li>
  ))}
</ul>
  </div>

{/*clicking*/}


  {selectedProduct && (
  <div className="mt-6 border-t pt-4">
    <h3 className="text-md font-semibold mb-2">Nutrition Info (per 100g):</h3>
    <ul className="text-sm -ml 30 space-y-1">
      <li><strong>Energy:</strong> {selectedProduct.nutriments['energy-kcal_100g'] ?? 'N/A'} kcal</li>
      <li><strong>Fat:</strong> {selectedProduct.nutriments['fat_100g'] ?? 'N/A'} g</li>
      <li><strong>Sugars:</strong> {selectedProduct.nutriments['sugars_100g'] ?? 'N/A'} g</li>
      <li><strong>Proteins:</strong> {selectedProduct.nutriments['proteins_100g'] ?? 'N/A'} g</li>
      <li><strong>Salt:</strong> {selectedProduct.nutriments['salt_100g'] ?? 'N/A'} g</li>
    </ul>
    <button onClick={() => addItemToMeal(mealId, selectedProduct.code, 1)} className="mt-4 bg-gray-200 px-4 py-2 rounded hover:bg-gray-300"></button>
  </div>
)}


{/* showing meal */}


  {(mealId && mealShow !== null) && (
    <div className="mt-6 border-t pt-4">
    <h3 className="text-md font-semibold mb-2">Meal ingredients:</h3>
    <ul className="text-sm -ml 30 space-y-1"> 
      {mealShow.map((ingredient, index) => (
    <li key={index}>
          {ingredient.name}
        </li>))}
    </ul>
    </div>
    )}


{/* settings */}
  <div>
    <button
    onClick={() => setShowSettings(prev => !prev)}
    className="mt-4 px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-800">
  
    {showSettings ? 'Hide Settings' : 'Show Settings'}
  </button>


  {showSettings && <SettingsPanel onClose={() => setShowSettings(false)} />}
  </div>
  </>
)
  


  } 

export default MealCreator