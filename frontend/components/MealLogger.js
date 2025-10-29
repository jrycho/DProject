'use client';
import { useState, useEffect , createContext, useContext} from 'react';
import { logMeal, getLogsByDate } from '@/utils/log_meal';
import MealButton from '@/components/MealButton';
import SettingsComponent from '@/components/SettingsComponent';
import { fetchLogs} from "@/utils/fetchLogs"
import { getLastSettings } from '@/utils/getLastSettings';
import OptimizeButton from './OptimizeButton';



const MEAL_TYPES = ['Breakfast', 'Snack 1', 'Lunch', 'Snack 2', 'Dinner', 'Snack 3'];

export default function MealLogger() {
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [logs, setLogs] = useState([]);
    const [activeMealLog, setActiveMealLog] = useState(false);
    const [activeMealId, setActiveMealId] = useState(null);

    const [settingsObj, setSettingsObj] = useState(null); 
    const [LastSettings, setLastSettings] = useState(null);
    const [ready, setReady] = useState(false)


    const dateKey = selectedDate.toISOString().split('T')[0]


    function changeDay(days) {
        const newDate = new Date(selectedDate);
        newDate.setDate(newDate.getDate() + days);
        setSelectedDate(newDate);
    }


    useEffect(() => {


        fetchLogs(dateKey, setLogs);}, [dateKey]);
        console.log(logs);




    //function if not logged, log, if logged, find and set to active
    async function mealButtonClick(mealType, isLogged) {
    
    if (activeMealLog?.type_of_meal === mealType) {
    setActiveMealLog(null);
    setActiveMealId(null);
    return;
    }
   
    if (!isLogged) {
    const newLog = await  logMeal(mealType, dateKey);

    setLogs(prev => [...prev, newLog]);
    

    await fetchLogs(dateKey, setLogs);
    

    setActiveMealLog(newLog);
    setActiveMealId(newLog.meal_id);
    

    } else { 
        const existingLog = logs.find(log => log.date === dateKey && log.type_of_meal === mealType);
        setActiveMealLog(existingLog);
        setActiveMealId(existingLog.meal_id);
        console.log('active meal log:' +  activeMealLog?.meal_id ?? '(none)');
    }
    }


    return (
        <>

    {/* Day navigation */}
    <div className='flex justify-center gap-4 mb-4 bg-gray-600 min-h-10'>
        <button onClick={() => changeDay(-1)} 
                className="bg-gray-700 px-3 py-1 rounded hover:bg-gray-300 "
    >
        ◀ Previous
        </button>

        <div className='font-semibold text-lg flex justify-center mt-1.5'>
                {selectedDate.toLocaleDateString('en-EU', {
        weekday: 'long',
        month: 'short',
        day: 'numeric',
        })}
        </div>

        <button onClick={() => changeDay(1)}
        className='bg-gray-700 px-3 py-1 rounded hover:bg-gray-300'>
        Next ▶
    </button>
    </div>


<div
className='grid w-1/2 grid-cols-1 md:grid-cols-2 gap-100'>
    {/* Meal buttons */}
            <div className='flex flex-col gap-2'>
                {MEAL_TYPES.map(mealType => {
                    const log = logs.find(log => log.type_of_meal === mealType);
                      const isActive = activeMealLog && log?.meal_id && activeMealLog.meal_id === log.meal_id;
                    return (
                        <MealButton
                            key={mealType}
                            meal={mealType}
                            mealId = {activeMealId}
                            isLogged={!!log}
                            isActive={  activeMealLog  != null && log?.meal_id != null && activeMealLog.meal_id === log.meal_id}
                            onClick={() => mealButtonClick(mealType, !!log)}
                        />
                    );
                })}
            </div>
            <details>
    {/* Settings */}            
  <summary className=' flex cursor-pointer list-none items-center  gap-0 rounded-xl px-4 py-3
               text-sm font-medium bg-gray-400 min-h-7 text-gray-900 hover:bg-gray-500 w-60 mt-0
               focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500'>
    ⚙️ Settings
  </summary>
            <div style={{ padding: 24 }}>
                <SettingsComponent
                    // optional: override list
                    // properties={['calories', 'protein', 'carbs']}
                    // optional: prefill (null = OFF)
                    initial={null}
                    autosave = {ready}
                    onChange={(payload) => {
                        // live updates (good place to debounce + autosave)
                        //console.log('onChange payload:', payload)
                        setSettingsObj(payload);
                        }}
                    onSubmit={(payload) => {
                    // click “Save” in the component
                    console.log('onSubmit payload:', payload);
                    ;
                    // await fetch('/api/save', { method: 'POST', body: JSON.stringify(payload) })
            }}
      />
    </div></details>
    </div>


            <OptimizeButton
            mealId = {activeMealId}/>
        </>
    );

}

