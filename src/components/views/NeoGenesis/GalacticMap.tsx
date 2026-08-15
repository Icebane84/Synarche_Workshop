// [OMEGA AST Cleaned]: Tokenized design standards applied.
import React from "react";
import { OrganismStats, PlanetNode } from "./NeoGenesisConstants";
import { LivePill } from "@/components/ui/LivePill";

interface GalacticMapProps {
  stats: OrganismStats;
  planets: PlanetNode[];
  selectedPlanet: PlanetNode;
  onSelectPlanet: (planet: PlanetNode) => void;
  onColonizePlanet: (planet: PlanetNode) => void;
}

export const GalacticMap: React.FC<GalacticMapProps> = ({
  stats,
  planets,
  selectedPlanet,
  onSelectPlanet,
  onColonizePlanet,
}) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-appear">
      <div className="lg:col-span-7 space-y-4">
        <div className="bg-panel-bg/40 border border-purple-500/40 p-5 rounded-xl space-y-4 shadow-2xl backdrop-blur-md">
          <div className="flex justify-between items-center border-b border-white/10 pb-3">
            <div>
              <h3 className="text-xs font-bold text-purple-300 uppercase tracking-wider flex items-center gap-2">
                <span>🌌 GALACTIC EXOPLANET STAR CHART</span>
              </h3>
              <p className="text-[10px] text-white/40">
                Dispatch interstellar colony ships to expand your species across star systems
              </p>
            </div>
            <div className="text-right">
              <span className="text-[10px] text-white/40 uppercase block">Starlight Energy</span>
              <span className="text-lg font-bold text-purple-400">✨ {stats.starlight}</span>
            </div>
          </div>

          <div className="space-y-3">
            {planets.map((p) => {
              const isSelected = selectedPlanet.id === p.id;
              return (
                <div
                  key={p.id}
                  onClick={() => onSelectPlanet(p)}
                  className={`p-4 rounded-lg border transition-all duration-200 cursor-pointer flex items-center justify-between ${
                    isSelected
                      ? `${p.color} shadow-lg scale-[1.01]`
                      : "bg-deep-space/60 border-white/5 hover:border-white/20"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-10 h-10 rounded-full border ${p.color} flex items-center justify-center font-bold text-sm shadow-inner`}
                    >
                      🪐
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-white/90">{p.name}</h4>
                      <p className="text-[10px] text-white/50">{p.type}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded uppercase font-bold border ${
                        p.status === "Colonized"
                          ? "bg-green-500/20 text-green-400 border-green-500/30"
                          : "bg-white/5 text-white/40 border-white/10"
                      }`}
                    >
                      {p.status}
                    </span>
                    <span className="block text-[10px] text-amber-400 mt-1">{p.output}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="lg:col-span-5 space-y-4">
        <div className="bg-panel-bg/40 border border-cyan-500/40 p-5 rounded-xl space-y-5 shadow-2xl backdrop-blur-md">
          <div className="flex justify-between items-center border-b border-white/10 pb-3">
            <div>
              <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-wider">
                🪐 EXOPLANET INSPECTOR
              </h3>
              <p className="text-[10px] text-white/40">{selectedPlanet.name}</p>
            </div>
            <LivePill
              label={selectedPlanet.status}
              type={selectedPlanet.status === "Colonized" ? "active" : "fading"}
            />
          </div>

          <div className="space-y-3 text-xs">
            <div className="bg-deep-space p-3 rounded border border-white/5 space-y-2">
              <div className="flex justify-between">
                <span className="text-white/50">Planet Type:</span>
                <span className="text-white/90 font-semibold">{selectedPlanet.type}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/50">Population:</span>
                <span className="text-cyan-400 font-bold">
                  {selectedPlanet.population.toLocaleString()} Units
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/50">Resource Yield:</span>
                <span className="text-amber-400 font-bold">{selectedPlanet.output}</span>
              </div>
            </div>

            {selectedPlanet.status === "Unexplored" ? (
              <button
                onClick={() => onColonizePlanet(selectedPlanet)}
                disabled={stats.dna < selectedPlanet.cost}
                className="w-full min-h-[44px] py-3 bg-gradient-to-r from-purple-500/20 to-cyan-500/20 hover:from-purple-500/40 hover:to-cyan-500/40 border border-purple-400 text-purple-300 rounded-lg text-xs font-bold tracking-widest uppercase transition-all shadow-lg cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed flex flex-col items-center justify-center"
              >
                <span>🚀 DISPATCH COLONY SEEDER</span>
                <span className="text-[9px] text-amber-400 font-mono">
                  REQUIRES {selectedPlanet.cost} DNA
                </span>
              </button>
            ) : (
              <div className="bg-green-500/10 border border-green-500/30 text-green-300 p-3 rounded text-center text-xs">
                ✅ Active Interstellar Outpost Established & Generating Resources!
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
