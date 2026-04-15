import { NavigationItem } from "@/lib/types";

type SidebarProps = {
  items: NavigationItem[];
};

export function Sidebar({ items }: SidebarProps) {
  return (
    <aside className="hidden w-64 flex-col border-r border-slate-800/80 bg-slate-950/80 px-4 py-6 backdrop-blur-xl lg:flex">
      <p className="px-3 text-xs font-semibold uppercase tracking-[0.24em] text-cyan-300/70">Navigation</p>
      <nav className="mt-4 space-y-1">
        {items.map((item, index) => {
          const active = index === 0;
          return (
            <button
              key={item.key}
              className={[
                "w-full rounded-xl px-3 py-2.5 text-left text-sm font-medium transition",
                active
                  ? "bg-cyan-400/10 text-cyan-200 shadow-[inset_0_0_0_1px_rgba(34,211,238,0.35)]"
                  : "text-slate-400 hover:bg-slate-800/70 hover:text-slate-100",
              ].join(" ")}
            >
              {item.label}
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
