"use client";

import { useEffect, useMemo, useState } from "react";
import { saveSettings } from "@/utils/saveSettings";
import { useDebouncedEffect } from "@/utils/useDebouncedEffect";
import { getLastSettings } from "@/utils/getLastSettings";
import GuideButton from "@/components/GuideButton";

const PROPS = ["calories", "protein", "carbs", "fats", "saturated_fat", "salt"];

function formatPropertyLabel(prop) {
  return prop
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export default function OptimizationSettingsForm({
  properties = PROPS,
  meal_type,
  onChange,
  onSubmit,
}) {
  const N = properties.length;

  const [propSel, setPropSel] = useState(Array(N).fill(null));
  const [target_goal, setTargetGoal] = useState(Array(N).fill(null));
  const [excess_weights, setExcessWeights] = useState(Array(N).fill(null));
  const [slack_weights, setSlackWeights] = useState(Array(N).fill(null));

  const [loaded, setLoaded] = useState(false);
  const [autosaveOn, setAutosaveOn] = useState(false);

  useEffect(() => {
    let cancel = false;

    (async () => {
      try {
        const saved = await getLastSettings(meal_type);
        if (cancel || !saved) return;

        const sel = Array(N).fill(null);
        const tg = Array(N).fill(null);
        const ew = Array(N).fill(null);
        const sw = Array(N).fill(null);

        const names = saved.optimized_properties ?? [];
        const T = saved.target_goal ?? [];
        const E = saved.excess_weights ?? [];
        const S = saved.slack_weights ?? [];

        names.forEach((name, idx) => {
          const i = properties.indexOf(name);
          if (i !== -1) {
            sel[i] = name;
            tg[i] = Number(T[idx] ?? 0);
            ew[i] = Number(E[idx] ?? 0);
            sw[i] = Number(S[idx] ?? 0);
          }
        });

        setPropSel(sel);
        setTargetGoal(tg);
        setExcessWeights(ew);
        setSlackWeights(sw);
        setLoaded(true);
        setAutosaveOn(true);
      } catch (e) {
        setLoaded(true);
      }
    })();

    return () => {
      cancel = true;
    };
  }, [N, meal_type, properties]);

  const isActive = (i) => propSel[i] !== null;

  const toggle = (i) => {
    const on = isActive(i);
    const nextName = on ? null : properties[i];
    const nextVal = on ? null : 0;

    setPropSel((a) => a.map((x, k) => (k === i ? nextName : x)));
    setTargetGoal((a) => a.map((x, k) => (k === i ? nextVal : x)));
    setExcessWeights((a) => a.map((x, k) => (k === i ? nextVal : x)));
    setSlackWeights((a) => a.map((x, k) => (k === i ? nextVal : x)));
  };

  const setAt = (setter, i, val) =>
    setter((a) => a.map((x, k) => (k === i ? Number(val) : x)));

  const settings = useMemo(() => {
    const optimized_properties = [];
    const tg = [];
    const ew = [];
    const sw = [];

    for (let i = 0; i < properties.length; i++) {
      if (propSel[i] !== null) {
        optimized_properties.push(properties[i]);
        tg.push(target_goal[i] ?? 0);
        ew.push(excess_weights[i] ?? 0);
        sw.push(slack_weights[i] ?? 0);
      }
    }

    return {
      optimized_properties,
      target_goal: tg,
      excess_weights: ew,
      slack_weights: sw,
    };
  }, [properties, propSel, target_goal, excess_weights, slack_weights]);

  useEffect(() => {
    onChange?.(settings);
    console.log("settings:", settings);
  }, [settings, onChange]);

  useDebouncedEffect(
    () => {
      if (!autosaveOn) return;
      if (!meal_type) return;
      if (settings.optimized_properties.length === 0) return;
      saveSettings(settings, meal_type);
    },
    [autosaveOn, settings, meal_type],
    500,
  );

  return (
    <div className="z-[90] rounded-l-xl bg-gray-700 w-[20rem] md:w-[45rem] fixed right-0 top-1/2 -translate-y-1/2 shadow max-h-[60vh] overflow-y-auto custom-scrollbar">
      <div className="px-3 pt-3 md:px-6 md:pt-4 flex justify-end">
        <GuideButton guideKey="mealLoggerSettings" buttonText="?" />
      </div>
      <div className="grid gap">
        {properties.map((p, i) => {
          const active = isActive(i);

          return (
            <div
              key={p}
              className="flex flex-col md:flex-row items-start gap-1.5 md:gap-3 mt-3 mb-3 px-3 md:px-0 md:ml-10"
            >
              <button
                type="button"
                onClick={() => toggle(i)}
                className={
                  active
                    ? "flex items-center justify-center text-center leading-none bg-green-600 text-white text-xs md:text-xl px-3 py-2 rounded w-32 md:w-64 h-8 md:h-12"
                    : "flex items-center justify-center text-center leading-none bg-green-600 text-black text-xs md:text-xl px-3 py-2 rounded w-32 md:w-64 h-8 md:h-12"
                }
              >
                {active ? "✓" : "●"} {formatPropertyLabel(p)}
              </button>

              {active ? (
                <div className="flex items-start gap-1">
                  <input
                    type="number"
                    min="1"
                    value={target_goal[i] ?? ""}
                    onChange={(e) => setAt(setTargetGoal, i, e.target.value)}
                    onFocus={(e) => e.target.select()}
                    onMouseUp={(e) => e.preventDefault()}
                    className="border rounded px-2 py-1 bg-white text-black w-20 mt-3"
                  />
                  <span className="w-12 text-right text-sm mt-3">excess</span>
                  <input
                    type="range"
                    min="0"
                    max="10"
                    value={excess_weights[i] ?? ""}
                    onChange={(e) => setAt(setExcessWeights, i, e.target.value)}
                    className="w-13 rotate-270 mt-3 custom-range"
                  />
                  <span className="w-12 text-right text-sm mt-3">slack</span>
                  <input
                    type="range"
                    min="0"
                    max="10"
                    value={slack_weights[i] ?? ""}
                    onChange={(e) => setAt(setSlackWeights, i, e.target.value)}
                    className="w-13 rotate-270 mt-3 custom-range"
                  />
                </div>
              ) : (
                <div />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
