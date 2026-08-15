import React from "react";
import { useUserContext, USER_THEME } from "@/core/useUserContext";
import { usePlayerState } from "@/core/hooks/usePlayerState";
import { useMemoryFeed } from "@/core/hooks/useMemoryFeed";
import { useActionLog } from "@/core/hooks/useActionLog";
import { StatBar } from "@/components/ui/StatBar";
import { LivePill } from "@/components/ui/LivePill";

export const DashboardView: React.FC = () => {
  const { userId, activeUser } = useUserContext();
  const theme = USER_THEME[activeUser];
  
  const { player, stats, isLoading: playerLoading } = usePlayerState(userId);
  const { memories, isLoading: memoriesLoading } = useMemoryFeed();
  const { entries: actionLogs } = useActionLog();

  const recentMemories = memories.slice(0, 5);

  return (
    <div className="space-y-6 animate-appear">
      {/* Top Banner section */}
      <div 
        className="elevation-panel p-6 border rounded-lg bg-panel-bg relative overflow-hidden"
        style={{ borderColor: theme.accent + '20' }}
      >
        <div className="absolute top-0 right-0 p-4 font-mono text-[9px] text-white/10 uppercase tracking-widest">
          Sovereign Node Overlord
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold tracking-widest uppercase mb-1">
              Welcome back, <span style={{ color: theme.accent }}>{activeUser}</span>
            </h2>
            <p className="text-xs text-white/50 font-mono">
              Identity Node: <span className="text-white/80">{userId}</span>
            </p>
          </div>
          <div className="flex items-center gap-3">
            <LivePill label="Coherent" type="active" />
            <LivePill label="Substrate Connected" type="info" />
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* LEVEL */}
        <div className="bg-panel-bg/40 border border-white/5 p-4 rounded-lg font-mono">
          <div className="text-[10px] text-chrome mb-1">EXPERIENCE SCALE</div>
          {playerLoading ? (
            <div className="h-10 flex items-center text-white/30 animate-pulse">Querying...</div>
          ) : (
            <div>
              <div className="text-2xl font-bold text-white/90 mb-2">
                Lvl {player?.level ?? 1}
              </div>
              <StatBar
                label="XP Progress"
                value={player?.xp ?? 0}
                max={((player?.level ?? 1) * 1000)}
                colorClass="bg-chris-amber"
                showDetails={false}
              />
              <div className="text-[10px] text-white/40 mt-1 text-right">
                {player?.xp ?? 0} / {((player?.level ?? 1) * 1000)} XP
              </div>
            </div>
          )}
        </div>

        {/* COHERENCE INDEX */}
        <div className="bg-panel-bg/40 border border-white/5 p-4 rounded-lg font-mono">
          <div className="text-[10px] text-chrome mb-1">COHERENCE INDEX</div>
          {playerLoading ? (
            <div className="h-10 flex items-center text-white/30 animate-pulse">Querying...</div>
          ) : (
            <div>
              <div className="text-2xl font-bold text-white/90 mb-2">
                {stats?.coherence_index ?? 0}%
              </div>
              <StatBar
                label="Alignment"
                value={stats?.coherence_index ?? 0}
                max={100}
                colorClass="bg-coherence-indigo"
                showDetails={false}
              />
              <div className="text-[10px] text-white/40 mt-1 text-right">
                Resonance Drift: {100 - (stats?.coherence_index ?? 0)}%
              </div>
            </div>
          )}
        </div>

        {/* STARDUST */}
        <div className="bg-panel-bg/40 border border-white/5 p-4 rounded-lg font-mono">
          <div className="text-[10px] text-chrome mb-1">STARDUST LEDGER</div>
          {playerLoading ? (
            <div className="h-10 flex items-center text-white/30 animate-pulse">Querying...</div>
          ) : (
            <div>
              <div className="text-2xl font-bold text-white/90 mb-1" style={{ color: theme.accent }}>
                ✨ {stats?.stardust_available ?? 0}
              </div>
              <div className="text-[10px] text-white/40 mt-2">
                Current spending capacity on cognitive directives.
              </div>
            </div>
          )}
        </div>

        {/* SYNERGY */}
        <div className="bg-panel-bg/40 border border-white/5 p-4 rounded-lg font-mono">
          <div className="text-[10px] text-chrome mb-1">SYNERGY SCORE</div>
          {playerLoading ? (
            <div className="h-10 flex items-center text-white/30 animate-pulse">Querying...</div>
          ) : (
            <div>
              <div className="text-2xl font-bold text-white/90 mb-2">
                {stats?.synergy ?? 0}%
              </div>
              <StatBar
                label="Interoperability"
                value={stats?.synergy ?? 0}
                max={100}
                colorClass="bg-synergy-emerald"
                showDetails={false}
              />
              <div className="text-[10px] text-white/40 mt-1 text-right">
                Node Interaction Rate
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main dashboard content area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Side: Recent Memory Entries */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-semibold tracking-[0.2em] text-white/60 uppercase">
              RECENT MEMORY CHIPS
            </h3>
            <span className="text-[10px] text-chrome font-mono">Live Sync</span>
          </div>

          <div className="space-y-3">
            {memoriesLoading ? (
              <div className="text-xs text-white/30 animate-pulse py-4">Defragmenting memory space...</div>
            ) : recentMemories.length === 0 ? (
              <div className="bg-panel-bg/25 border border-white/5 p-6 rounded-lg text-center text-xs text-white/30 italic">
                No memory fragments detected. Create one in the Memory Palace.
              </div>
            ) : (
              recentMemories.map((memory, idx) => (
                <div 
                  key={memory.id || `memory-${idx}`} 
                  className="bg-panel-bg/40 border border-white/5 p-4 rounded-lg hover:border-white/10 transition-colors font-mono"
                >
                  <div className="flex items-center justify-between mb-2">
                    <LivePill label={memory.domain} type="info" />
                    <span className="text-[10px] text-white/30">
                      Layer {memory.memory_layer ?? 1} • {memory.state}
                    </span>
                  </div>
                  <p className="text-xs text-white/80 leading-relaxed font-sans mb-1">
                    {memory.content}
                  </p>
                  <div className="text-[9px] text-white/30 flex items-center justify-between mt-2 pt-2 border-t border-white/[0.03]">
                    <span>Score: {memory.activation_score ?? 0}</span>
                    <span>Hash: {memory.content_hash?.substring(0, 12)}...</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right Side: Quick Substrate Health */}
        <div className="space-y-4">
          <h3 className="text-xs font-semibold tracking-[0.2em] text-white/60 uppercase">
            SUBSTRATE TELEMETRY
          </h3>

          <div className="bg-panel-bg/40 border border-white/5 rounded-lg p-4 font-mono space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-white/40">Status:</span>
                <span className="text-green-400 font-semibold uppercase">Nominal</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-white/40">Telemetry Load:</span>
                <span className="text-white/80">0.02 Hz</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-white/40">Active Shards:</span>
                <span className="text-white/80">19 Tables</span>
              </div>
            </div>

            <div className="border-t border-white/5 pt-3">
              <div className="text-[10px] text-chrome mb-2">CORE METRICS</div>
              <div className="space-y-3">
                <StatBar
                  label="Adaptability"
                  value={stats?.adaptability ?? 0}
                  colorClass="bg-adapt-amber"
                />
                <StatBar
                  label="Ascension"
                  value={stats?.form_ascension_state ?? 0}
                  colorClass="bg-form-ascension"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
