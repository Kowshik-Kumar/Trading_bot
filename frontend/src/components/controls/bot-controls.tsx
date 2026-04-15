"use client";

import { useMemo, useState } from "react";

import { Panel } from "@/components/ui/panel";
import { StrategyOption } from "@/lib/types";

type BotControlsProps = {
  options: StrategyOption[];
};

export function BotControls({ options }: BotControlsProps) {
  const [isRunning, setIsRunning] = useState(true);
  const [strategy, setStrategy] = useState<StrategyOption>(options[2]);

  const statusLabel = useMemo(() => (isRunning ? "Bot Running" : "Bot Stopped"), [isRunning]);

  return (
    <Panel className="p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-slate-500">Controls</p>
          <h3 className="mt-1 text-base font-semibold text-slate-100">Automation Engine</h3>
        </div>
        <span
          className={[
            "rounded-full px-3 py-1 text-xs font-semibold",
            isRunning ? "bg-emerald-400/15 text-emerald-300" : "bg-rose-400/15 text-rose-300",
          ].join(" ")}
        >
          {statusLabel}
        </span>
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-[1fr_auto_auto]">
        <select
          value={strategy}
          onChange={(event) => setStrategy(event.target.value as StrategyOption)}
          className="w-full rounded-xl border border-slate-700 bg-slate-900 px-3 py-2.5 text-sm text-slate-100 outline-none ring-cyan-300/30 transition focus:ring-2"
        >
          {options.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
        <button
          onClick={() => setIsRunning(true)}
          className="rounded-xl bg-cyan-400 px-4 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300"
        >
          Start Bot
        </button>
        <button
          onClick={() => setIsRunning(false)}
          className="rounded-xl border border-slate-600 px-4 py-2.5 text-sm font-semibold text-slate-200 transition hover:border-rose-300/60 hover:text-rose-200"
        >
          Stop Bot
        </button>
      </div>
    </Panel>
  );
}
