import React from "react";
import { useActionLog } from "@/core/hooks/useActionLog";
import { useUserContext } from "@/core/useUserContext";

export const ActivityRail: React.FC = () => {
  const { entries, isLoading, error } = useActionLog();
  const { activeUser } = useUserContext();

  return (
    <div className="w-[280px] h-full flex flex-col bg-deep-space border-l border-white/5 font-mono select-none">
      {/* Header */}
      <div className="h-14 px-4 border-b border-white/5 flex items-center justify-between">
        <span className="text-xs font-semibold tracking-[0.2em] text-celestial-blue flex items-center gap-2">
          <span className="w-1.5 h-1.5 bg-celestial-blue rounded-full animate-pulse"></span>
          KINETIC SHARD STREAM
        </span>
        <span className="text-[10px] text-white/40">LIVE</span>
      </div>

      {/* Log list */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 scrollbar-thin">
        {isLoading ? (
          <div className="text-xs text-white/30 animate-pulse">Initializing quantum stream...</div>
        ) : error ? (
          <div className="text-xs text-red-500/80">Stream error: {error}</div>
        ) : entries.length === 0 ? (
          <div className="text-xs text-white/20 italic">No kinetic records found.</div>
        ) : (
          entries.map((entry, idx) => {
            const dateStr = entry.timestamp 
              ? new Date(entry.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }) 
              : "00:00:00";

            return (
              <div 
                key={entry.id || `entry-${entry.timestamp || idx}-${idx}`} 
                className="text-xs border-b border-white/5 pb-2 animate-appear hover:bg-white/[0.02] p-1 rounded transition-colors"
              >
                <div className="flex items-center justify-between gap-1 text-[10px] text-white/30 mb-0.5">
                  <span className="text-white/40">{dateStr}</span>
                  <span className="uppercase text-[9px] px-1 bg-white/5 rounded border border-white/5 max-w-[120px] truncate">
                    {entry.action_type}
                  </span>
                </div>
                <div className="text-white/80 leading-normal line-clamp-3 select-text">
                  {entry.outcome || (entry.payload ? JSON.stringify(entry.payload) : "")}
                </div>
                {entry.triggered_by && (
                  <div className="text-[9px] text-celestial-blue/60 mt-0.5 text-right font-mono font-semibold">
                    &gt; {entry.triggered_by}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
