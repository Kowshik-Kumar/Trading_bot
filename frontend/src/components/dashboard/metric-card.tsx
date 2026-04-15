import { DashboardMetric } from "@/lib/types";
import { Panel } from "@/components/ui/panel";

type MetricCardProps = {
  metric: DashboardMetric;
};

export function MetricCard({ metric }: MetricCardProps) {
  const trendColor = {
    up: "text-emerald-300",
    down: "text-rose-300",
    neutral: "text-amber-300",
  }[metric.trend];

  return (
    <Panel className="p-4">
      <p className="text-xs font-medium uppercase tracking-[0.2em] text-slate-500">{metric.title}</p>
      <p className="mt-3 text-2xl font-semibold tracking-tight text-slate-100">{metric.value}</p>
      <div className="mt-3 flex items-center justify-between">
        <span className={["text-sm font-semibold", trendColor].join(" ")}>{metric.delta}</span>
        <span className="text-xs text-slate-500">{metric.subtitle}</span>
      </div>
    </Panel>
  );
}
