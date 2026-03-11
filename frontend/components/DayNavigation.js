"use client";
import { useState, useEffect, useCallback } from "react";
import Calendar from "./Calendar";
export default function DateSelector({ onClickDays }) {
  const [selectedDate, setSelectedDate] = useState(new Date());

  const changeDay = useCallback(
    (days) => {
      setSelectedDate((prev) => {
        const d = new Date(prev);
        d.setDate(d.getDate() + days);

        // use the fresh date here

        return d;
      });
    },
    [onClickDays, setSelectedDate],
  );

  useEffect(() => {
    onClickDays?.({ selectedDate });
  }, [selectedDate, onClickDays]);
  return (
    <>
      {/* Day navigation */}
      <div className="w-full bg-gray-600 h-[2.5rem] mb-2">
        <div className="flex flex-wrap justify-center mb-4 min-h-10 items-center border border-green-600">
          <button
            onClick={() => changeDay(-1)}
            className="bg-gray-700 px-3 py-1 rounded hover:bg-gray-500 text-white min-w-[110px] h-8 "
          >
            ◀ Previous
          </button>
          <Calendar value={selectedDate} onChange={setSelectedDate} />
          {/*
        <div className='font-semibold text-lg flex justify-center mt-1.5 text-white'>
                {selectedDate.toLocaleDateString('en-EU', {
        weekday: 'long',
        month: 'short',
        day: 'numeric',
        })}
        </div>*/}

          <button
            onClick={() => changeDay(1)}
            className="bg-gray-700 px-3 py-1 rounded hover:bg-gray-500 text-white min-w-[80px] h-8"
          >
            Next ▶
          </button>
        </div>
      </div>
    </>
  );
}
