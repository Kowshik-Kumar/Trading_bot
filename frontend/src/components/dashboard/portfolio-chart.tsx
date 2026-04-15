"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Panel } from "@/components/ui/panel";
import { PricePoint } from "@/lib/types";

type PortfolioChartProps = {
  data: PricePoint[];
};

export function PortfolioChart({ data }: PortfolioChartProps) {
  return (
    <Panel className="h-[340px] min-h-[340px] p-4">
      <div className="mb-4 flex items-start justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-slate-500">Market Trend</p>
          <h2 className="mt-1 text-lg font-semibold text-slate-100">Live Asset Snapshot</h2>
        </div>
        <p className="text-xs text-slate-500">BTC / ETH / SOL</p>
      </div>
      <ResponsiveContainer width="100%" height="85%" minWidth={300} minHeight={220}>
        <LineChart data={data} margin={{ top: 10, right: 4, left: -18, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 6" stroke="#1f2937" />
          <XAxis dataKey="time" tick={{ fill: "#64748b", fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: "#475569", fontSize: 12 }} axisLine={false} tickLine={false} width={50} />
          <Tooltip
            contentStyle={{
              background: "rgba(10, 17, 31, 0.95)",
              border: "1px solid rgba(56, 189, 248, 0.25)",
              borderRadius: "12px",
              color: "#e2e8f0",
            }}
          />
          <Line type="monotone" dataKey="btc" stroke="#22d3ee" strokeWidth={2.4} dot={false} />
          <Line type="monotone" dataKey="eth" stroke="#4ade80" strokeWidth={2.2} dot={false} />
          <Line type="monotone" dataKey="sol" stroke="#f59e0b" strokeWidth={2.2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </Panel>
  );
}
