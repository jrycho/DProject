'use client';

import MealLogger from '@/components/MealLogger';
import Navbar from '@/components/Navbar';
import JsonTextViewerIngredients from '@/components/JsonTextViewerIngredients'
import JsonTextViewerMacros from '@/components/JsonTextViewerMacros';
import OptimizeButton from '@/components/OptimizeButton';
import {MealIdCtx} from '@/utils/mealIdCtx'
import ProtectedPage from '@/components/ProtectedPage';
import Threads from '@/components/Threads';
import { useState, useCallback} from 'react';

export default function Page() {

  const [activeMealId, setActiveMealId] = useState(null);
  const [settingsObj, setSettingsObj] = useState(null);
  const [ mealWeights, setMealWeights ] = useState([  {
    "barcode": "Placeholder",
    "name": "No items",
    "grams": "-"
  }]);
  const [ mealMacros, setMealMacros ] = useState({"No macros yet":"-"});


  // One callback that receives both
  const handleChange = useCallback(({ activeMealId, settingsObj }) => {
    setActiveMealId(activeMealId);
    setSettingsObj(settingsObj);
    console.log("Parent activeMealId:", activeMealId)
  }, []);

    const handleOptimizeResults = useCallback(({ mealWeights, mealMacros }) => {
      setMealWeights(Array.isArray(mealWeights) ? [...mealWeights] : []);
      console.log(mealWeights)
      setMealMacros(mealMacros ? { ...mealMacros } : {});
      console.log(mealMacros)
  }, []);

  return (

    <ProtectedPage>
      <main className="p-4">
      <Navbar />
      
        <div
          className="fixed inset-0 -z-10 pointer-events-none"
          aria-hidden
                >
                    
  {/* threads on top */}
          <div className="absolute inset-0">
              <div style={{ width: '100%', height: '600px', position: 'relative' }}>
              <Threads
                amplitude={1}
                distance={0}
                enableMouseInteraction={true}
              />
              </div>
          </div>
        </div>
<div class="grid grid-cols-3 grid-rows-2 gap-6">
  <div className='col-start-1 col-end-4'>
      <MealLogger onChange={handleChange} />
        <div className='mt-3'>
        <OptimizeButton
            onResults={handleOptimizeResults}
            mealId = {activeMealId}/>
        </div>            
  </div>
        <div className='col-start-2 row-start-2'><JsonTextViewerIngredients inputText={mealWeights} /></div>
        <div className='col-start-3 row-start-2'><JsonTextViewerMacros inputText={mealMacros} /></div>
  </div>
    </main>
    
    </ProtectedPage>

  );
}