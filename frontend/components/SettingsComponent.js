'use client';
import { useMemo, useState } from 'react';
import { useEffect } from 'react';
import { saveSettings } from '@/utils/saveSettings';
import {useDebouncedEffect} from '@/utils/useDebouncedEffect';
import { getLastSettings } from '@/utils/getLastSettings';

const PROPS = ['calories', 'protein', 'carbs', 'fats', 'saturated_fats', 'salt', 'test'];

// If you want to pass `properties` from a parent, keep the prop.
// Otherwise, it will default to PROPS.
export default function OptimizationSettingsForm({ properties = PROPS, onChange, onSubmit}) {
  
  const N = properties.length;

  // 4 arrays: selector (string|null) + three value arrays (number|null)
  const [propSel, setPropSel] = useState(Array(N).fill(null))
  const [target_goal, setTargetGoal] = useState(Array(N).fill(null))
  const [excess_weights, setExcessWeights] = useState(Array(N).fill(null))
  const [slack_weights, setSlackWeights] = useState(Array(N).fill(null))


  const [loaded, setLoaded] = useState(false);      // block onChange/autosave until true
  const [autosaveOn, setAutosaveOn] = useState(false); // internal switch you can enable after load

  // ---- Async function balast ----
  useEffect(() => {
    let cancel = false; //set flags
    (async () => {
      try {
        const saved = await getLastSettings(); // await the data
        if (cancel || !saved) return;

        // expand compact saved payload into per-index arrays
        const sel = Array(N).fill(null);
        const tg  = Array(N).fill(null);
        const ew  = Array(N).fill(null);
        const sw  = Array(N).fill(null);

        const names = saved.optimized_properties ?? [];
        const T = saved.target_goal ?? [];
        const E = saved.excess_weights ?? [];
        const S = saved.slack_weights ?? [];

        
        // creating arrays to fill and iterate them
        names.forEach((name, idx) => {
          const i = properties.indexOf(name);
          if (i !== -1) {
            sel[i] = name;                // turn this row ON
            tg[i]  = Number(T[idx] ?? 0);
            ew[i]  = Number(E[idx] ?? 0);
            sw[i]  = Number(S[idx] ?? 0);
          }
        });

        setPropSel(sel);
        setTargetGoal(tg);
        setExcessWeights(ew);
        setSlackWeights(sw);
        setLoaded(true);
        // enable autosave 
        setAutosaveOn(true);
      } catch (e) {
        // if loading fails, still unblock UI;
        setLoaded(true);
      }
    })();
    return () => { cancel = true; };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [N]); // re-hydrate if properties length changes



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


  useDebouncedEffect(()=> {
    if (!autosaveOn) return
    if (settings.optimized_properties.length === 0) return 
    saveSettings(settings)},[autosaveOn, settings], 500);













  return (<div className="rounded-xl bg-gray-700 w-180 p-6 shadow ml-0"><div className="grid gap  ">
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
            ? "bg-green-600 text-white px-3 py-2 rounded w-64 h-16 "
            : "bg-green-600 text-black px-3 py-2 rounded w-64"}
        >
          {active ? "✔" : "●"} {p}
        </button>

        {/* Right: inputs for this prop (only when active) */}
        {active ? (
          <div className="flex items-start gap-1 ">
            {/* <strong className="text-white">{propSel[i]}</strong>*/}

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
              className="w-13 rotate-270 mt-3"
              
            />
            <span className="w-12 text-right text-sm mt-3">slack</span>

            <input
              type="range"
              min="0"
              max="10"
              value={slack_weights[i] ?? ""}
              onChange={(e) => setAt(setSlackWeights, i, e.target.value)}
              className="w-13 rotate-270 mt-3"
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
    
