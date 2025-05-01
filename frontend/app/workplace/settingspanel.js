'use client';

import React, { useState } from 'react';

const SettingsPanel = () => {
  const [expanded, setExpanded] = useState(null);
  const [settings, setSettings] = useState({
    calories: { target: '', slack: 10, excess: 10 },
    carbs: { target: '', slack: 10, excess: 10 },
    protein: { target: '', slack: 10, excess: 10 },
    fats: { target: '', slack: 10, excess: 10 },
    saturatedFats: { target: '', slack: 10, excess: 10 },
    sugars: { target: '', slack: 10, excess: 10 },
    sodium: { target: '', slack: 10, excess: 10 },
  });

  const nutrients = Object.keys(settings);

  return (
    <div className="p-4 mt-4 border-s-green-600 rounded bg-gray-400 shadow-md">
      <h2 className="text-2xl font-semibold mb-4">Meal Target settings</h2>
    
    {nutrients.map((nutrient) => (
      <div key={nutrient} className="mb-4">
        <button
        onClick={()=>
          setExpanded((prev) => prev === nutrient ? null : nutrient)
        }
        className='w-full text-left font-medium text-s-green-600'>
          {nutrient.charAt(0).toUpperCase() + nutrient.slice(1)}
        </button>

        {expanded === nutrient && (
          <div className="mt-2 space-y-2 border-l border-gray-200 pl-4">
              <div>
                <label className="block text-sm font-medium">Target</label>
                <input
                  type="number"
                  value={settings[nutrient].target}
                  onChange={(e) =>
                    setSettings((prev) => ({
                      ...prev,
                      [nutrient]: {
                        ...prev[nutrient],
                        target: Number(e.target.value),
                      },
                    }))
                  }
                  className="w-full p-1 border rounded"
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Min</label>
                <input
                  type="range"
                  min="0"
                  max="10"
                  value={settings[nutrient].slack}
                  onChange={(e) =>
                    setSettings((prev) => ({
                      ...prev,
                      [nutrient]: {
                        ...prev[nutrient],
                        slack: Number(e.target.value),
                      },
                    }))
                  }
                  className="w-full"
                />
                <p className="text-sm text-gray-500">Value: {settings[nutrient].slack}</p>
              </div>

              <div>
                <label className="block text-sm font-medium">Max</label>
                <input
                  type="range"
                  min="0"
                  max="10"
                  value={settings[nutrient].excess}
                  onChange={(e) =>
                    setSettings((prev) => ({
                      ...prev,
                      [nutrient]: {
                        ...prev[nutrient],
                        excess: Number(e.target.value),
                      },
                    }))
                  }
                  className="w-full"
                />
                <p className="text-sm text-gray-500">Value: {settings[nutrient].excess}</p>
              </div>
            </div>
          )}
        </div>
      ))}
      </div>
      )
    }
      


export default SettingsPanel;