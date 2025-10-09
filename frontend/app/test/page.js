'use client';
import { useMemo, useState } from 'react';
import { useEffect } from 'react';

const PROPS = ['calories', 'protein', 'carbs', 'fat', 'saturated_fats', 'salt', 'test'];

// If you want to pass `properties` from a parent, keep the prop.
// Otherwise, it will default to PROPS.
export default function OptimizationSettingsForm({ properties = PROPS, initial = {}, onChange, onSubmit }) {
  const N = properties.length;

  // 4 arrays: selector (string|null) + three value arrays (number|null)
  const [propSel, setPropSel] = useState(() => initial.propSel ?? Array(N).fill(null));
  const [target_goal, setTargetGoal] = useState(() => initial.target_goal ?? Array(N).fill(null));
  const [excess_weights, setExcessWeights] = useState(() => initial.excess_weights ?? Array(N).fill(null));
  const [slack_weights, setSlackWeights] = useState(() => initial.slack_weights ?? Array(N).fill(null));


  const isActive = (i) => propSel[i] !== null;

  const toggle = (i) => {
    const on = isActive(i);
    const nextName = on ? null : properties[i]; // string name when ON
    const nextVal  = on ? null : 0;             // start numbers at 0

    setPropSel(a       => a.map((x, k) => (k === i ? nextName : x)));
    setTargetGoal(a    => a.map((x, k) => (k === i ? nextVal  : x)));
    setExcessWeights(a => a.map((x, k) => (k === i ? nextVal  : x)));
    setSlackWeights(a  => a.map((x, k) => (k === i ? nextVal  : x)));
  };

  const setAt = (setter, i, val) =>
    setter(a => a.map((x, k) => (k === i ? Number(val) : x)));

  // If you ever need a compact payload (drop nulls), memoize it here:
  const settings = useMemo(() => {
    const optimized_properties = [];
    const tg = [], ew = [], sw = [];
    for (let i = 0; i < properties.length; i++) {
      if (propSel[i] !== null) {
        optimized_properties.push(properties[i]);
        tg.push(target_goal[i] ?? 0);
        ew.push(excess_weights[i] ?? 0);
        sw.push(slack_weights[i] ?? 0);
      }
    }
    return { optimized_properties, target_goal: tg, excess_weights: ew, slack_weights: sw };
  }, [properties, propSel, target_goal, excess_weights, slack_weights]);

 useEffect(() => {
    onChange?.(settings);
    console.log('settings:' , settings);
    
  }, [settings, onChange]);

  return (<div className="rounded-xl bg-gray-700 w-180 p-6 shadow"><div className="grid gap-4 mt-3 ">
  {properties.map((p, i) => {
    const active = isActive(i);
    return (
      <div
        key={p}
        className="items-start gap-3 flex mb-3 ml-30" 
      >
        {/* Left: the toggle button */}
        <button
          type="button"
          onClick={() => toggle(i)}
          className={active
            ? "bg-green-600 text-white px-3 py-2 rounded w-64 h-32 "
            : "bg-green-600 text-black px-3 py-2 rounded w-64"}
        >
          {active ? "ON" : "OFF"} — {p}
        </button>

        {/* Right: inputs for this prop (only when active) */}
        {active ? (
          <div className="grid gap-2 ">
            <strong className="text-white">{propSel[i]}</strong>

            <input
              type="number"
              value={target_goal[i] ?? ""}
              onChange={(e) => setAt(setTargetGoal, i, e.target.value)}
              onFocus={(e) => e.target.select()}
              onMouseUp={(e) => e.preventDefault()} 
              className="border rounded px-2 py-1 bg-white text-black w-56"
            />

            <input
              type="range"
              min="0"
              max="10"
              value={excess_weights[i] ?? ""}
              onChange={(e) => setAt(setExcessWeights, i, e.target.value)}
              className="w-56"
            />

            <input
              type="range"
              min="0"
              max="10"
              value={slack_weights[i] ?? ""}
              onChange={(e) => setAt(setSlackWeights, i, e.target.value)}
              className="w-56"
            />
          </div>
        ) : (
          // keeps the grid structure aligned when inactive
          <div />
        )}
      </div>
    );
  })}
</div>
</div>
);}
    
