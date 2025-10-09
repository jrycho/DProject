import { useEffect } from "react";

export async function useDebouncedEffect(useOnFunction,rerunWhenChanges,  delay ) {
  useEffect(() => {
    const t = setTimeout(useOnFunction, delay);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...rerunWhenChanges, delay]);
}

