const { useState } = require("react")

const PROPS = ['calories', 'protein', 'carbs', 'fat', 'saturated_fats', 'salt']

function OptimizationSettingsForm({ properties }) {
    const N = properties.length;
    const [propSel, setPropSel] = useState(Array(N).fill(null))
    const [target_goal, setTargeGoal] = useState(Array(N).fill(null)) 
    const [excess_weights, setExcessWeights] = useState(Array(N).fill(null))
    const [slack_weights, setSlackWeights] = useState(Array(N).fill(null))

    const settings = useMemo(
        ()=> ({
        optimized_properties: properties,
        target_goal,
        excess_weights,
        slack_weights,
    }),[properties, target_goal, excess_weights, slack_weights]); //with Memo build json with arrays, watch on change
}

const isActive = (i) => propSel[i] != null;

const toggle = (i) => {
    const on = isActive(i);
    const NextName = on ? null : PROPS[i]
    const nextVal = on ? null : 0;

    setPropSel(a => a.map((x,k) => ( k===i ? NextName : x)));
    setTargeGoal(a => a.map((x,k) => ( k===i ? NextVal : x)));
    setExcessWeights(a => a.map((x,k) => ( k===i ? NextVal : x)));
    setSlackWeights(a => a.map((x,k) => ( k===i ? NextVal : x)));


const setAt = (setter, i, val) =>
    setter(a => a.map((x, k) => (k === i ? Number(val) : x)));

return (
    <div style={{ display: "grid", gap: 12, maxWidth: 720 }}>
      {/* buttons: fixed index = position in PROPS */}
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        {PROPS.map((p, i) => (
          <button key={p} onClick={() => toggle(i)}>
            {isActive(i) ? "ON" : "OFF"} — {p} (idx {i})
          </button>
        ))}
      </div>

      {/* show inputs only when ON */}
      {PROPS.map((p, i) =>
        !isActive(i) ? null : (
          <div key={p} style={{ display: "grid", gridTemplateColumns: "180px 1fr 1fr 1fr", gap: 8, alignItems: "center" }}>
            <strong>{propsSel[i]}</strong>
            <input type="number" value={target[i]} onChange={e => setAt(setTarget, i, e.target.value)} />
            <input type="number" value={excess[i]} onChange={e => setAt(setExcess, i, e.target.value)} />
            <input type="number" value={slack[i]}  onChange={e => setAt(setSlack,  i, e.target.value)} />
          </div>
        )
      )}

      {/* debug: see all four arrays */}
      <pre>{JSON.stringify({ propsSel, target, excess, slack }, null, 2)}</pre>
    </div>
  );
}