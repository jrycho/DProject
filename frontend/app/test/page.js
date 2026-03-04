'use client';
import GraphComponent from "@/components/GraphComponent";
import Dashboard from "@/components/Dashboard";


export default function Page() {
  const date = "2026-03-02"
  return (
    <>
      <div>
        <Dashboard date={date} />
      </div>
    </>
  );
}
