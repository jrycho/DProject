"use client";

import MealLogger from "@/components/MealLogger";
import Navbar from "@/components/Navbar";
import JsonTextViewerIngredients from "@/components/JsonTextViewerIngredients";
import JsonTextViewerMacros from "@/components/JsonTextViewerMacros";
import ProtectedPage from "@/components/ProtectedPage";
import { useState, useCallback } from "react";
import DateSelector from "@/components/DayNavigation";
import ThreadsBackground from "@/components/ThreadsBackground";
import Dashboard from "@/components/Dashboard";

export default function Page() {
  const [activeMealId, setActiveMealId] = useState(null);
  const [activeMealType, setActiveMealType] = useState(null);
  const [settingsObj, setSettingsObj] = useState(null);
  const [mealWeights, setMealWeights] = useState([
    {
      barcode: "Placeholder",
      name: "No items",
      grams: "-",
    },
  ]);
  const [mealMacros, setMealMacros] = useState({ "No macros yet": "-" });
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [dashboardRefresh, setDashboardRefresh] = useState(0);

  const handleChange = useCallback(
    ({ activeMealId, activeMealType, settingsObj }) => {
      setActiveMealId(activeMealId);
      setSettingsObj(settingsObj);
      setActiveMealType(activeMealType);
    },
    [],
  );

  const handleOptimizeResults = useCallback(({ mealWeights, mealMacros }) => {
    setMealWeights(Array.isArray(mealWeights) ? [...mealWeights] : []);
    setMealMacros(mealMacros ? { ...mealMacros } : {});
    setDashboardRefresh((prev) => prev + 1);
  }, []);

  const handleChangeDay = useCallback(({ selectedDate }) => {
    setSelectedDate(selectedDate);
  }, []);

  return (
    <ProtectedPage>
      <main className="p-4 pt-10 overflow-x-hidden">
        <Navbar className="relative z-[100]" />

        <div className="fixed inset-0 -z-10 pointer-events-none" aria-hidden>
          <div className="absolute inset-0">
            <div
              style={{ width: "100%", height: "600px", position: "relative" }}
            >
              <ThreadsBackground
                amplitude={1}
                distance={0}
                enableMouseInteraction={true}
              />
            </div>
          </div>
        </div>

        <div className="flex justify-center">
          <DateSelector onClickDays={handleChangeDay} />
        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-3 md:grid-rows-2">
          <div className="order-2 justify-center md:col-start-2 md:col-end-4 md:row-start-1 md:row-end-2">
            <Dashboard date={selectedDate} refresh={dashboardRefresh} />
          </div>

          <div className="order-4 justify-center md:col-start-1 md:col-end-2 md:row-start-1 md:row-end-3 z-[90]">
            <MealLogger
              onChange={handleChange}
              selectedDate={selectedDate}
              setMealWeights={setMealWeights}
              setMealMacros={setMealMacros}
              onOptimizeResults={handleOptimizeResults}
            />
          </div>

          <div className="order-5 justify-center md:col-start-2 md:col-end-3 md:row-start-2 md:row-end-3">
            <JsonTextViewerIngredients inputText={mealWeights} />
          </div>

          <div className="order-6 justify-center md:col-start-3 md:col-end-4 md:row-start-2">
            <JsonTextViewerMacros inputText={mealMacros} />
          </div>
        </div>
      </main>
    </ProtectedPage>
  );
}
