'use client'
import { useState,useEffect, useCallback } from "react";
export default function DateSelector({onClickDays}){
    const [selectedDate, setSelectedDate] = useState(new Date());


const changeDay = useCallback((days)=> {
        setSelectedDate(prev => {
            const d = new Date(prev);
            d.setDate(d.getDate() + days);

            // use the fresh date here
            

            return d;
        });
        }, [onClickDays, setSelectedDate]);

    useEffect(() => {
        onClickDays?.({ selectedDate });
    }, [selectedDate, onClickDays]);
        return (
        <>

    {/* Day navigation */}
    <div className='flex justify-center gap-4 mb-4 bg-gray-600 min-h-10 '>
        <button onClick={() => changeDay(-1)} 
                className="bg-gray-700 px-3 py-1 rounded hover:bg-gray-300 text-white "
    >
        ◀ Previous
        </button>

        <div className='font-semibold text-lg flex justify-center mt-1.5 text-white'>
                {selectedDate.toLocaleDateString('en-EU', {
        weekday: 'long',
        month: 'short',
        day: 'numeric',
        })}
        </div>

        <button onClick={() => changeDay(1)}
        className='bg-gray-700 px-3 py-1 rounded hover:bg-gray-300 text-white'>
        Next ▶
    </button>
    </div>
    </>
)}