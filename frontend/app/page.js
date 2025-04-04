'use client';

import { useEffect, useState } from 'react';

export default function Home() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((error) => console.error('Error:', error));
  }, []);

  return (
    <div className="container mx-auto mt-10 text-center">
      <h1 className="text-4xl font-bold">Next.js + FastAPI</h1>
      <p className="mt-4 text-xl">{message || "Loading message..."}</p>
      <AddItemByName/>
    </div>
  );
}


export  function AddItemByName (){
  const [keyword, setKeyword] = useState('');
  const [items, setItems] = useState([]);
  const handleSubmit = async () => {
    const res = await fetch ('http://127.0.0.1:8000/add_items_by_name/?keyword=' + keyword, {
      method: 'POST',
    });
  // Convert the response into a JavaScript object
  const data = await res.json();

  // Update the `items` state with the data returned by FastAPI
  setItems(data.selected_items);
};

// This part defines what the component will show (the UI)
return (
  <div className="p-4">
    {/* This is a text box for the user to type the keyword */}
    <input
      type="text"
      placeholder="Enter keyword"        // Gray text shown before the user types
      value={keyword}                    // The current value of the input is `keyword`
      onChange={(e) => setKeyword(e.target.value)} // Update `keyword` when user types
      className="border p-2 mr-2"        // Tailwind CSS styles (optional)
    />

    {/* This is a button that runs `handleSubmit` when clicked */}
    <button
      onClick={handleSubmit}
      className="bg-green-300 text-black px-4 py-2"
    >
      Add Items
    </button>

    {/* If we have any items returned from the backend, show them as a list */}
    {items.length > 0 && (
      <ul className="mt-4">
        {/* Loop through each item in the list and show it in a <li> */}
        {items.map((item, index) => (
          <li key={index} className="border-b py-1">
            {item} {/* Display the item name */}
          </li>
        ))}
      </ul>
    )}
  </div>
);
};

