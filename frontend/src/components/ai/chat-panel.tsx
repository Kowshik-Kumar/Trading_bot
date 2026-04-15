"use client";

import { FormEvent, useMemo, useState } from "react";

import { Panel } from "@/components/ui/panel";
import { ChatMessage } from "@/lib/types";

type ChatPanelProps = {
  initialMessages: ChatMessage[];
};

export function ChatPanel({ initialMessages }: ChatPanelProps) {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [prompt, setPrompt] = useState("");

  const submitDisabled = useMemo(() => prompt.trim().length === 0, [prompt]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = prompt.trim();
    if (!trimmed) {
      return;
    }

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      text: trimmed,
      timestamp: "Now",
    };

    const assistantMessage: ChatMessage = {
      id: `assistant-${Date.now() + 1}`,
      role: "assistant",
      text: "Signal check complete: risk budget allows one additional BTC scalp entry with 0.8% stop-loss.",
      timestamp: "Now",
    };

    setMessages((current) => [...current, userMessage, assistantMessage]);
    setPrompt("");
  };

  return (
    <Panel className="flex h-[460px] flex-col p-0">
      <div className="border-b border-slate-800/80 px-4 py-3">
        <p className="text-xs font-medium uppercase tracking-[0.2em] text-slate-500">AI Copilot</p>
        <h3 className="mt-1 text-base font-semibold text-slate-100">Trading Intelligence</h3>
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto px-4 py-4">
        {messages.map((message) => (
          <article
            key={message.id}
            className={[
              "max-w-[90%] rounded-2xl px-3 py-2.5 text-sm",
              message.role === "assistant"
                ? "bg-slate-800/80 text-slate-200"
                : "ml-auto bg-cyan-400/15 text-cyan-100",
            ].join(" ")}
          >
            <p>{message.text}</p>
            <p className="mt-1 text-[11px] text-slate-500">{message.timestamp}</p>
          </article>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="border-t border-slate-800/80 p-3">
        <div className="flex gap-2">
          <input
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
            placeholder="Ask AI about position sizing, risk, or entries..."
            className="w-full rounded-xl border border-slate-700 bg-slate-900 px-3 py-2.5 text-sm text-slate-100 outline-none ring-cyan-300/30 transition placeholder:text-slate-500 focus:ring-2"
          />
          <button
            type="submit"
            disabled={submitDisabled}
            className="rounded-xl bg-cyan-400 px-4 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Send
          </button>
        </div>
      </form>
    </Panel>
  );
}
