import { Panel } from "@/components/ui/panel";
import { TradeRecord } from "@/lib/types";

type TradeHistoryTableProps = {
  trades: TradeRecord[];
};

export function TradeHistoryTable({ trades }: TradeHistoryTableProps) {
  return (
    <Panel className="p-0">
      <div className="flex items-center justify-between border-b border-slate-800/80 px-4 py-3">
        <h3 className="text-base font-semibold text-slate-100">Trade History</h3>
        <span className="text-xs text-slate-500">Last 24 hours</span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[680px] text-left text-sm">
          <thead className="bg-slate-900/40 text-xs uppercase tracking-[0.18em] text-slate-500">
            <tr>
              <th className="px-4 py-3 font-medium">Order ID</th>
              <th className="px-4 py-3 font-medium">Pair</th>
              <th className="px-4 py-3 font-medium">Side</th>
              <th className="px-4 py-3 font-medium">Amount</th>
              <th className="px-4 py-3 font-medium">Price</th>
              <th className="px-4 py-3 font-medium">P&amp;L</th>
              <th className="px-4 py-3 font-medium">Status</th>
              <th className="px-4 py-3 font-medium">Time</th>
            </tr>
          </thead>
          <tbody>
            {trades.map((trade) => (
              <tr key={trade.id} className="border-t border-slate-800/70 text-slate-300">
                <td className="px-4 py-3 text-slate-400">{trade.id}</td>
                <td className="px-4 py-3 font-medium text-slate-100">{trade.pair}</td>
                <td className="px-4 py-3">
                  <span
                    className={[
                      "rounded-full px-2 py-1 text-xs font-semibold",
                      trade.side === "Buy" ? "bg-emerald-400/15 text-emerald-300" : "bg-rose-400/15 text-rose-300",
                    ].join(" ")}
                  >
                    {trade.side}
                  </span>
                </td>
                <td className="px-4 py-3">{trade.amount}</td>
                <td className="px-4 py-3">{trade.price}</td>
                <td
                  className={[
                    "px-4 py-3 font-semibold",
                    trade.pnl.startsWith("+") ? "text-emerald-300" : "text-rose-300",
                  ].join(" ")}
                >
                  {trade.pnl}
                </td>
                <td className="px-4 py-3 text-slate-400">{trade.status}</td>
                <td className="px-4 py-3 text-slate-500">{trade.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Panel>
  );
}
