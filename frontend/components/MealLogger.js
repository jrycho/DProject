"use client";
import { useState, useEffect, createContext, useContext } from "react";
import { logMeal, getLogsByDate } from "@/utils/log_meal";
import MealButton from "@/components/MealButton";
import SettingsComponent from "@/components/SettingsComponent";
import { fetchLogs } from "@/utils/fetchLogs";
import { getLastSettings } from "@/utils/getLastSettings";
import OptimizeButton from "./OptimizeButton";
import {
  getOptimizationMacros,
  getOptimizationWeights,
} from "@/utils/getResults";
import { getOptimizationWeightsAndMacros } from "@/utils/getResults";

const MEAL_TYPES = [
  "Breakfast",
  "Snack 1",
  "Lunch",
  "Snack 2",
  "Dinner",
  "Snack 3",
];

export default function MealLogger({
  onChange,
  selectedDate,
  setMealWeights,
  setMealMacros,
  onOptimizeResults,
}) {
  const [logs, setLogs] = useState([]);
  const [activeMealLog, setActiveMealLog] = useState(false);
  const [activeMealId, setActiveMealId] = useState(null);

  const [settingsObj, setSettingsObj] = useState(null);
  const [LastSettings, setLastSettings] = useState(null);
  const [ready, setReady] = useState(false);

  const dateKey = selectedDate.toISOString().split("T")[0];

  const [activeMealType, setActiveMealType] = useState("Breakfast");

  useEffect(() => {
    setActiveMealLog(null);
    setActiveMealId(null);
    fetchLogs(dateKey, setLogs);
  }, [dateKey]);
  console.log(logs);

  useEffect(() => {
    onChange?.({ activeMealId, activeMealType, settingsObj });
  }, []);

  useEffect(() => {
    onChange?.({ activeMealId, activeMealType, settingsObj });
  }, [activeMealId, activeMealType, settingsObj, onChange]);

  useEffect(() => {
    async function loadOptimization() {
      if (!activeMealId) {
        setMealWeights([
          { barcode: "Placeholder", name: "No items", grams: "-" },
        ]);
        setMealMacros({ "No macros yet": "-" });
        return;
      }

      try {
        const { weights, macros } =
          await getOptimizationWeightsAndMacros(activeMealId);

        console.log(weights);
        console.log(macros);

        setMealWeights(weights);
        setMealMacros(macros);
      } catch (err) {
        console.error("Failed to load optimization:", err);

        setMealWeights([
          { barcode: "Placeholder", name: "No items", grams: "-" },
        ]);
        setMealMacros({ "No macros yet": "-" });
      }
    }

    loadOptimization();
  }, [activeMealId]);

  async function mealButtonClick(mealType, isLogged) {
    if (activeMealLog?.type_of_meal === mealType) {
      setActiveMealLog(null);
      setActiveMealId(null);
      return;
    }
    setActiveMealType(mealType);

    if (!isLogged) {
      const newLog = await logMeal(mealType, dateKey);

      setLogs((prev) => [...prev, newLog]);

      await fetchLogs(dateKey, setLogs);

      setActiveMealLog(newLog);
      setActiveMealId(newLog.meal_id);
    } else {
      const existingLog = logs.find(
        (log) => log.date === dateKey && log.type_of_meal === mealType,
      );
      setActiveMealLog(existingLog);
      setActiveMealId(existingLog.meal_id);
      console.log("active meal log:" + activeMealLog?.meal_id ?? "(none)");
    }
  }

  return (
    <>
      <div className="grid w-full  grid-cols-1 md:grid-cols-2 ">
        <div className="mx-auto md:mx-0 w-full flex flex-col gap-2">
          {MEAL_TYPES.map((mealType) => {
            const log = logs.find((log) => log.type_of_meal === mealType);
            const isActive =
              activeMealLog &&
              log?.meal_id &&
              activeMealLog.meal_id === log.meal_id;
            return (
              <MealButton
                key={mealType}
                meal={mealType}
                mealId={log?.meal_id ?? null}
                isLogged={!!log}
                isActive={
                  activeMealLog != null &&
                  log?.meal_id != null &&
                  activeMealLog.meal_id === log.meal_id
                }
                onClick={() => mealButtonClick(mealType, !!log)}
              />
            );
          })}

          <OptimizeButton
            onResults={onOptimizeResults}
            mealId={activeMealId}
            mealType={activeMealType}
          />
        </div>

        <details className="group">
          <summary
            className="
  fixed top-1/2 -translate-y-1/2 z-[90]
  right-0
  translate-x-0 group-open:-translate-x-[20rem] md:group-open:-translate-x-[45rem]
  transition-transform duration-180
  [writing-mode:vertical-rl] rotate-180
  cursor-pointer list-none
  px-8 py-3
  text-3xl font-medium text-white
  bg-green-400 hover:bg-green-500
  [--cut:12px]
  [clip-path:polygon(0%_0,80%_0,100%_10%,100%_90%,80%_100%,100%_100%,0_100%,0_0%)]
"
          >
            Settings
          </summary>

          <div className="p-4 md:p-6 max-w-full overflow-x-hidden">
            <SettingsComponent
              className="transition-transform duration-300"
              initial={null}
              autosave={ready}
              onChange={(payload) => {
                setSettingsObj(payload);
              }}
              meal_type={activeMealType}
              onSubmit={(payload) => {
                console.log("onSubmit payload:", payload);
              }}
            />
          </div>
        </details>
      </div>
    </>
  );
}
