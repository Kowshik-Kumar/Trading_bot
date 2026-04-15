import { ChatPanel } from "@/components/ai/chat-panel";
import { MetricCard } from "@/components/dashboard/metric-card";
import { PortfolioChart } from "@/components/dashboard/portfolio-chart";
import { BotControls } from "@/components/controls/bot-controls";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopNavbar } from "@/components/layout/top-navbar";
import { TradeHistoryTable } from "@/components/trades/trade-history-table";
import {
  chartData,
  dashboardMetrics,
  initialChat,
  navigationItems,
  strategyOptions,
  tradeHistory,
} from "@/lib/mock-data";

export default function Home() {
  return (
    <div className="relative min-h-screen bg-slate-950 text-slate-100">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_12%_12%,rgba(34,211,238,0.18),transparent_32%),radial-gradient(circle_at_88%_0%,rgba(59,130,246,0.14),transparent_28%),radial-gradient(circle_at_55%_80%,rgba(16,185,129,0.1),transparent_30%)]" />

      <div className="relative mx-auto flex min-h-screen max-w-[1600px]">
        <Sidebar items={navigationItems} />

        <main className="flex w-full flex-col">
          <TopNavbar />

          <section className="border-b border-slate-800/70 px-4 py-3 lg:hidden">
            <div className="flex gap-2 overflow-x-auto pb-1">
              {navigationItems.map((item, index) => (
                <button
                  key={item.key}
                  className={[
                    "whitespace-nowrap rounded-full px-3 py-1.5 text-sm",
                    index === 0
                      ? "bg-cyan-400/15 text-cyan-100"
                      : "bg-slate-800/80 text-slate-400",
                  ].join(" ")}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </section>

          <section className="grid gap-4 p-4 sm:gap-5 sm:p-6">
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {dashboardMetrics.map((metric) => (
                <MetricCard key={metric.title} metric={metric} />
              ))}
            </div>

            <div className="grid gap-4 xl:grid-cols-[1.7fr_1fr]">
              <PortfolioChart data={chartData} />
              <BotControls options={strategyOptions} />
            </div>

            <div className="grid gap-4 xl:grid-cols-[1.7fr_1fr]">
              <TradeHistoryTable trades={tradeHistory} />
              <ChatPanel initialMessages={initialChat} />
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}
