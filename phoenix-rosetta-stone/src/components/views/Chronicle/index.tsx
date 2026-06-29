import React, { useState, useEffect } from "react";
import { supabase } from "@/core/supabase";
import { LivePill } from "@/components/ui/LivePill";

export const ChronicleView: React.FC = () => {
  const [episodes, setEpisodes] = useState<any[]>([]);
  const [messages, setMessages] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchChronicle = async () => {
    setIsLoading(true);

    const [eps, msgs] = await Promise.all([
      supabase.from("episodes").select("*").order("started_at", { ascending: false }).limit(20),
      supabase.from("conversation_history").select("*").order("created_at", { ascending: false }).limit(40),
    ]);

    setEpisodes(eps.data ?? []);
    setMessages((msgs.data ?? []).reverse()); // display in chronological order
    setIsLoading(false);
  };

  useEffect(() => {
    fetchChronicle();
  }, []);

  return (
    <div className="space-y-6 animate-appear">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div>
          <h2 className="text-sm font-bold tracking-[0.25em] text-white uppercase">
            CHRONICLE FEED
          </h2>
          <p className="text-[11px] text-white/40 font-mono mt-0.5">
            Temporal record of episodes, cognitive events, and agent-user dialogues
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Episodes List */}
        <div className="space-y-4">
          <h3 className="text-xs font-semibold tracking-[0.25em] text-white/60 uppercase font-mono">
            COGNITIVE EPISODES
          </h3>

          <div className="space-y-3">
            {isLoading ? (
              <div className="text-xs text-white/30 animate-pulse font-mono py-4">Reconstructing timelines...</div>
            ) : episodes.length === 0 ? (
              <div className="bg-panel-bg/25 border border-white/5 p-6 rounded-lg text-center text-xs text-white/30 italic font-mono">
                No episodes cataloged.
              </div>
            ) : (
              episodes.map((ep) => (
                <div
                  key={ep.id}
                  className="bg-panel-bg/40 border border-white/5 p-4 rounded-lg font-mono text-xs space-y-2 hover:border-white/10 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white/90">Ep. #{ep.id}</span>
                    <LivePill label={ep.status || "Completed"} type="info" />
                  </div>
                  <p className="text-[11px] text-white/60 leading-relaxed font-sans">
                    {ep.summary || "Summary generation pending."}
                  </p>
                  <div className="flex justify-between text-[9px] text-white/30 pt-2 border-t border-white/[0.03]">
                    <span>Coherence Delta: {ep.coherence_delta || "+0"}%</span>
                    <span>Memories Locked: {ep.memory_count || "0"}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right Column: Dialogue Transcripts */}
        <div className="lg:col-span-2 space-y-4 flex flex-col h-[600px]">
          <h3 className="text-xs font-semibold tracking-[0.25em] text-white/60 uppercase font-mono">
            CONVERSATION TRANSCRIPTS
          </h3>

          <div className="flex-1 bg-panel-bg/30 border border-white/5 rounded-lg p-4 overflow-y-auto space-y-4 font-mono text-xs flex flex-col scrollbar-thin select-text">
            {isLoading ? (
              <div className="text-xs text-white/30 animate-pulse py-8 text-center">Tapping dialogue buffer...</div>
            ) : messages.length === 0 ? (
              <div className="text-xs text-white/20 italic py-8 text-center">No conversational messages logged.</div>
            ) : (
              messages.map((msg) => {
                const isUser = msg.sender === "Chris";
                return (
                  <div
                    key={msg.id}
                    className={`max-w-[85%] rounded p-3 ${
                      isUser
                        ? "bg-chris-amber/5 border border-chris-amber/20 self-start text-left"
                        : "bg-axion-indigo/5 border border-axion-indigo/20 self-end text-left"
                    }`}
                  >
                    <div className="flex items-center justify-between gap-4 text-[9px] text-white/30 mb-1">
                      <span className={`font-bold ${isUser ? "text-chris-amber" : "text-axion-indigo"}`}>
                        {msg.sender || "System"}
                      </span>
                      <span>
                        {msg.created_at ? new Date(msg.created_at).toLocaleTimeString() : ""}
                      </span>
                    </div>
                    <p className="text-white/80 leading-relaxed font-sans text-xs select-text whitespace-pre-wrap">
                      {msg.content || msg.message}
                    </p>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
