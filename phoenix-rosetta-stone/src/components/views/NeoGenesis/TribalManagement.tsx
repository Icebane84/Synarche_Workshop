import React from "react";
import { OrganismStats, TribalStructure } from "./NeoGenesisConstants";
import { LivePill } from "@/components/ui/LivePill";

interface TribalManagementProps {
  stats: OrganismStats;
  tribalStructures: TribalStructure[];
  logs: string[];
  onBuildStructure: (struct: TribalStructure) => void;
}

export const TribalManagement: React.FC<TribalManagementProps> = ({
  stats,
  tribalStructures,
  logs,
  onBuildStructure,
}) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-appear font-mono">
      <div className="lg:col-span-7 space-y-4">
        <div className="bg-panel-bg/40 border border-amber-500/40 p-5 rounded-xl space-y-5 shadow-2xl backdrop-blur-md">
          <div className="flex justify-between items-center border-b border-white/10 pb-3">
            <div>
              <h3 className="text-xs font-bold text-amber-300 uppercase tracking-wider flex items-center gap-2">
                <span>🏛️ STAGE II: TRIBAL HABITAT & TERRITORIAL MAP</span>
              </h3>
              <p className="text-[10px] text-white/40">
                Manage population growth and balance ecological harmony with industrial expansion
              </p>
            </div>
            <div className="text-right">
              <span className="text-[10px] text-white/40 uppercase block">Tribal Population</span>
              <span className="text-lg font-bold text-amber-400">👥 {stats.population.toLocaleString()}</span>
            </div>
          </div>

          {/* Ecology vs Industry Balance Meter */}
          <div className="grid grid-cols-2 gap-4 bg-deep-space p-4 rounded-lg border border-white/5">
            <div className="space-y-1">
              <div className="flex justify-between text-[11px]">
                <span className="text-green-400 font-semibold">🌿 ECOLOGICAL HARMONY</span>
                <span className="text-white font-bold">{stats.ecology}%</span>
              </div>
              <div className="w-full h-2 bg-black/60 rounded-full overflow-hidden border border-white/10">
                <div
                  className="h-full bg-green-500 transition-all duration-300"
                  style={{ width: `${stats.ecology}%` }}
                />
              </div>
            </div>

            <div className="space-y-1">
              <div className="flex justify-between text-[11px]">
                <span className="text-amber-400 font-semibold">⚙️ INDUSTRIAL OUTPUT</span>
                <span className="text-white font-bold">{stats.industry}%</span>
              </div>
              <div className="w-full h-2 bg-black/60 rounded-full overflow-hidden border border-white/10">
                <div
                  className="h-full bg-amber-500 transition-all duration-300"
                  style={{ width: `${stats.industry}%` }}
                />
              </div>
            </div>
          </div>

          {/* Tribal Structures Construct Grid */}
          <div className="space-y-3">
            <h4 className="text-[10px] text-white/40 uppercase tracking-wider font-semibold">
              Tribal Habitat Constructs
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {tribalStructures.map((st) => (
                <div
                  key={st.id}
                  className="bg-deep-space p-3.5 rounded-lg border border-white/5 space-y-2 flex flex-col justify-between"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{st.icon}</span>
                      <div>
                        <h5 className="text-xs font-bold text-white/90">{st.name}</h5>
                        <span className="text-[10px] text-white/40 block">{st.type}</span>
                      </div>
                    </div>
                    <span className="text-xs font-bold text-amber-400 bg-white/5 px-2 py-0.5 rounded border border-white/10">
                      x{st.count}
                    </span>
                  </div>

                  <p className="text-[10px] text-cyan-300">{st.effect}</p>

                  <button
                    onClick={() => onBuildStructure(st)}
                    disabled={stats.dna < st.cost}
                    className="w-full min-h-[44px] py-1.5 bg-amber-500/15 hover:bg-amber-500/30 border border-amber-500/40 text-amber-300 rounded text-xs font-semibold disabled:opacity-30 disabled:cursor-not-allowed transition-all cursor-pointer flex items-center justify-center gap-1"
                  >
                    <span>CONSTRUCT</span>
                    <span className="text-[9px] text-amber-400 font-mono">({st.cost} DNA)</span>
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="lg:col-span-5 space-y-4">
        <div className="bg-panel-bg/40 border border-cyan-500/40 p-5 rounded-xl space-y-5 shadow-2xl backdrop-blur-md">
          <div className="flex justify-between items-center border-b border-white/10 pb-3">
            <div>
              <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-wider">
                📜 TRIBAL CHRONICLE & GOVERNANCE
              </h3>
              <p className="text-[10px] text-white/40">Sovereign Species Progression</p>
            </div>
            <LivePill label="STAGE II" type="active" />
          </div>

          <div className="space-y-3 text-xs">
            <div className="bg-deep-space p-3 rounded border border-white/5 space-y-2">
              <div className="flex justify-between">
                <span className="text-white/50">Sovereign Intellect:</span>
                <span className="text-cyan-400 font-bold">Level {stats.intelligence}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/50">Habitat Capacity:</span>
                <span className="text-white/90 font-semibold">
                  {(
                    (tribalStructures.find((s) => s.id === "S1")?.count || 0) * 1000
                  ).toLocaleString()}{" "}
                  Units
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/50">Next Evolution Tier:</span>
                <span className="text-purple-400 font-bold">Interstellar Starfarer</span>
              </div>
            </div>

            <div className="bg-deep-space p-3 rounded-lg border border-white/5 space-y-1 text-[11px] text-white/70">
              <span className="text-[10px] text-white/30 uppercase block font-semibold mb-1">
                Tribal Event Chronicle
              </span>
              {logs.map((log, idx) => (
                <p key={idx} className={idx === 0 ? "text-amber-300 font-semibold" : "text-white/50"}>
                  {log}
                </p>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
