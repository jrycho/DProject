'use client';
import { useState, useEffect , createContext, useContext} from 'react';
import { logMeal, getLogsByDate } from '@/utils/log_meal';
import MealButton from '@/components/MealButton';
import SettingsComponent from '@/components/SettingsComponent';
import { fetchLogs} from "@/utils/fetchLogs"
import { getLastSettings } from '@/utils/getLastSettings';
import OptimizeButton from './OptimizeButton';




const MEAL_TYPES = ['Breakfast', 'Snack 1', 'Lunch', 'Snack 2', 'Dinner', 'Snack 3'];

export default function MealLogger( {onChange}) {
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [logs, setLogs] = useState([]);
    const [activeMealLog, setActiveMealLog] = useState(false);
    const [activeMealId, setActiveMealId] = useState(null);

    const [settingsObj, setSettingsObj] = useState(null); 
    const [LastSettings, setLastSettings] = useState(null);
    const [ready, setReady] = useState(false)


    const dateKey = selectedDate.toISOString().split('T')[0]




    useEffect(() => {


        fetchLogs(dateKey, setLogs);}, [dateKey]);
        console.log(logs);


    useEffect(() => {
            onChange?.({ activeMealId, settingsObj });
        }, []); // run once on mount

    useEffect(() => {
            onChange?.({ activeMealId, settingsObj });   // expose multiple consts on every change
        }, [activeMealId, settingsObj, onChange]);

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
    
    
    <details className="group">
    {/* Settings */}            
        <summary className="
            fixed  top-1/2 -translate-y-1/2
            right-0
            translate-x-0 group-open:-translate-x-180
            transition-transform duration-180
            [writing-mode:vertical-rl] rotate-180     /* vertical reading top→bottom */
            cursor-pointer list-none
            px-8 py-3
            text-3xl font-medium text-white 
            bg-green-400 hover:bg-green-500
            [--cut:12px]
            [clip-path:polygon(0%_0,80%_0,100%_10%,100%_90%,80%_100%,100%_100%,0_100%,0_0%)]
            focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500">
            Settings
        </summary>


                    <div style={{ padding: 24 }}
                    >
                        
                        <SettingsComponent
                            className='transition-transform duration-300'
                            initial={null}
                            autosave = {ready}
                            onChange={(payload) => {
                                setSettingsObj(payload);
                                }}
                            onSubmit={(payload) => {
                            // click “Save” in the component
                            console.log('onSubmit payload:', payload);
                            ;
                            // await fetch('/api/save', { method: 'POST', body: JSON.stringify(payload) })
                    }}
            />
            </div>
    </details>
    </div>

       

        </>
    );

}

