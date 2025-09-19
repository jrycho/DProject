'use client';
import { useState, useEffect } from 'react';
import { logMeal, getLogsByDate } from '@/utils/log_meal';
import MealButton from '@/components/MealButton';
import { fetchLogs} from "@/utils/fetchLogs"

const MEAL_TYPES = ['Breakfast', 'Snack 1', 'Lunch', 'Snack 2', 'Dinner', 'Snack 3'];


export default function MealLogger() {
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [logs, setLogs] = useState([]);
    const [activeMealLog, setActiveMealLog] = useState(false);



    const dateKey = selectedDate.toISOString().split('T')[0]
    //const dateKey = selectedDate.toISOString().split('T')[0]+`T11:00:00Z`;

    function changeDay(days) {
        const newDate = new Date(selectedDate);
        newDate.setDate(newDate.getDate() + days);
        setSelectedDate(newDate);
    }


    useEffect(() => {


        fetchLogs(dateKey, setLogs);}, [dateKey]);

    //function if not logged, log, if logged, find and set to active
    async function mealButtonClick(mealType, isLogged) {
    if (!isLogged) {
    const newLog = await  logMeal(mealType, dateKey);

    setLogs(prev => [...prev, newLog]);
    

    await fetchLogs(dateKey, setLogs);    

    setActiveMealLog(newLog);
    
    } else { 
        const existingLog = logs.find(log => log.date === dateKey && log.type_of_meal === mealType);
        setActiveMealLog(existingLog);
    }
    }



    return (
        <>
    {/* Day navigation */}
    <div className='flex justify-center gap-4 mb-4'>
        <button onClick={() => changeDay(-1)} 
                className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300"
    >
        ◀ Previous
        </button>

        <div className='font-semibold text-lg'>
                {selectedDate.toLocaleDateString('en-EU', {
        weekday: 'long',
        month: 'short',
        day: 'numeric',
        })}
        </div>

        <button onClick={() => changeDay(1)}
        className='bg-gray-200 px-3 py-1 rounded hover:bg-gray-300'>
        Next ▶
    </button>
    </div>



    {/* Meal buttons */}
            <div className='flex flex-col gap-2'>
                {MEAL_TYPES.map(mealType => {
                    const log = logs.find(log => log.type_of_meal === mealType);
                    return (
                        <MealButton
                            key={mealType}
                            meal={mealType}
                            isLogged={!!log}
                            onClick={() => mealButtonClick(mealType, !!log)}
                        />
                    );
                })}
            </div>
        </>
    );
}

