import { optimizeFunction } from "@/utils/optimizeFunction"
import { useState } from 'react'
import {useMealId} from '@/utils/mealIdCtx'


export default function OptimizeButton({mealId}){
      const [busy, setBusy] = useState(false)
      const disabled = busy || !mealId


        const handleOptimize = async () => {
            if (!mealId || busy) return
            const id = mealId;       // prefer context, fallback to prop
            if (!id || busy) return;                 // guard: no id or already running

            try {
            setBusy(true);
            await optimizeFunction(id);        
            } finally {
            setBusy(false);
            }
        };
    return(
        <div>
            <button
                
                className={"ml-30 w-40 min-h-10 bg-green-600 rounded-2xl "}
                onClick = {handleOptimize} //THIS WILL NEED SOME SAFETY SO SPAMMING IT WONT DO ANYTHING 
                disabled={disabled}
                
                >
                    Optimize
            </button>
            
        </div>
    )
}