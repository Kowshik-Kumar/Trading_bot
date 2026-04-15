export function TopNavbar() {
  return (
    <header className="sticky top-0 z-20 border-b border-slate-800/70 bg-slate-950/70 px-4 py-3 backdrop-blur-xl sm:px-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-500">Control Hub</p>
          <h1 className="mt-1 text-lg font-semibold tracking-tight text-slate-100 sm:text-xl">
            AI Trading Assistant
          </h1>
        </div>
        <div className="flex items-center gap-2 rounded-xl border border-cyan-300/20 bg-cyan-400/10 px-3 py-1.5 text-xs text-cyan-100">
          <span className="inline-flex h-2 w-2 rounded-full bg-emerald-400" />
          Bot latency 42ms
        </div>
      </div>
    </header>
  );
}
