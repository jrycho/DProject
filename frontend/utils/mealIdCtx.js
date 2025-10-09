"use client";
import { createContext, useContext } from "react";

const MealIdCtx = createContext(null);
export const useMealId = () => useContext(MealIdCtx);
