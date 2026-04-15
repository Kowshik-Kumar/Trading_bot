import { ReactNode } from "react";

type PanelProps = {
  children: ReactNode;
  className?: string;
};

export function Panel({ children, className = "" }: PanelProps) {
  return (
    <section
      className={[
        "rounded-2xl border border-slate-800/80 bg-[linear-gradient(140deg,rgba(15,23,42,0.92),rgba(8,14,28,0.96))] p-4 shadow-[0_0_0_1px_rgba(148,163,184,0.05),0_20px_35px_-20px_rgba(2,6,23,1)]",
        className,
      ].join(" ")}
    >
      {children}
    </section>
  );
}
