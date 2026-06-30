import React from "react";
import { OrganismStats } from "./NeoGenesisConstants";
import { LivePill } from "@/components/ui/LivePill";

interface EvoStatsPanelProps {
  stats: OrganismStats;
  audioEnabled: boolean;
  setAudioEnabled: (enabled: boolean) => void;
  onRegenerateHp: () => void;
  onAscendEra: () => void;
}

export const EvoStatsPanel: React.FC<EvoStatsPanelProps> = ({
  stats,
  audioEnabled,
  setAudioEnabled,
  onRegenerateHp,
  onAscendEra,
}) => {
  return (
    <div className="bg-panel-bg/40 border border-white/5 p-4 rounded-lg space-y-4 font-mono">
      <div className="flex justify-between items-center border-b border-white/10 pb-2.5">
        <h3 className="text-xs font-semibold text-white/70 uppercase tracking-wider">
          ORGANISM INDEX
        </h3>
        <button
          onClick={() => setAudioEnabled(!audioEnabled)}
          className="text-[10px] text-white/40 hover:text-white"
        >
          {audioEnabled ? "🔊 SOUNDS ON" : "🔇 SOUNDS OFF"}
        </button>
      </div>

      <div className="space-y-2 text-xs">
        <div className="flex justify-between">
          <span className="text-white/40">Era Stage:</span>
          <span className="text-green-400 font-bold uppercase">{stats.stage}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-white/40">DNA Pool:</span>
          <span className="text-cyan-400 font-bold">🧬 {stats.dna}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-white/40">Starlight Ledger:</span>
          <span className="text-amber-400 font-bold">✨ {stats.starlight}</span>
        </div>
        {stats.stage === "Galactic" && (
          <div className="flex justify-between">
            <span className="text-white/40">Total Population:</span>
            <span className="text-white/80">{stats.population.toLocaleString()}</span>
          </div>
        )}
      </div>

      <div className="space-y-3 pt-2">
        <div>
          <div className="flex justify-between text-[10px] text-chrome mb-1">
            <span>Cellular Integrity (HP)</span>
            <span>
              {stats.hp}/{stats.maxHp}
            </span>
          </div>
          <div className="w-full bg-deep-space rounded h-2 overflow-hidden border border-white/5">
            <div
              className={`h-full transition-all duration-300 ${
                stats.hp < 30 ? "bg-red-500" : "bg-emerald-500"
              }`}
              style={{ width: `${(stats.hp / stats.maxHp) * 100}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-[10px] text-chrome mb-1">
            <span>Evolutionary Readiness</span>
            <span>{stats.readiness}%</span>
          </div>
          <div className="w-full bg-deep-space rounded h-2 overflow-hidden border border-white/5">
            <div
              className="h-full bg-purple-500 transition-all duration-300"
              style={{ width: `${stats.readiness}%` }}
            />
          </div>
        </div>
      </div>

      <div className="pt-2 space-y-2">
        <button
          onClick={onRegenerateHp}
          disabled={stats.dna < 15 || stats.hp >= stats.maxHp}
          className="w-full py-1.5 bg-white/5 hover:bg-white/10 border border-white/10 text-white/80 rounded text-[11px] tracking-wider transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          REPAIR CELL MEMBRANE (Cost: 15 DNA)
        </button>

        <button
          onClick={onAscendEra}
          disabled={stats.readiness < 100}
          className="w-full py-2 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-400/50 text-purple-200 rounded text-xs tracking-widest font-bold transition-all disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer"
        >
          🌟 ASCEND ERA PHASE
        </button>
      </div>
    </div>
  );
};
