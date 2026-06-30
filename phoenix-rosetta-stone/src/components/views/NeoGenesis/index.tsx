import React, { useState, useEffect, useRef } from "react";
import {
  OrganismStats,
  TribalStructure,
  PlanetNode,
  INITIAL_PLANETS,
  INITIAL_TRIBAL_STRUCTURES,
} from "./NeoGenesisConstants";
import { CellularCanvas } from "./CellularCanvas";
import { TribalManagement } from "./TribalManagement";
import { GalacticMap } from "./GalacticMap";

export const NeoGenesisView: React.FC = () => {
  const [stats, setStats] = useState<OrganismStats>({
    hp: 100, maxHp: 100, dna: 20, starlight: 50, population: 120,
    ecology: 85, industry: 15, stage: "Cellular", speed: 2,
    armor: 1, ingestion: 1, intelligence: 1, readiness: 0,
  });

  const [activeViewMode, setActiveViewMode] = useState<"Cellular" | "Tribal" | "GalacticMap">("Cellular");
  const [tribalStructures, setTribalStructures] = useState<TribalStructure[]>(INITIAL_TRIBAL_STRUCTURES);
  const [planets, setPlanets] = useState<PlanetNode[]>(INITIAL_PLANETS);
  const [selectedPlanet, setSelectedPlanet] = useState<PlanetNode>(INITIAL_PLANETS[0]);
  const [audioEnabled, setAudioEnabled] = useState(false);
  const [logs, setLogs] = useState<string[]>([
    "Primordial genesis initiated. Beware of Predator ICES & Toxic Acid Biomes!",
  ]);
  const audioCtxRef = useRef<AudioContext | null>(null);

  const playSound = (type: "absorb" | "mutagen" | "hit" | "ascend" | "build") => {
    if (!audioEnabled) return;
    try {
      if (!audioCtxRef.current)
        audioCtxRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
      const ctx = audioCtxRef.current;
      if (ctx.state === "suspended") ctx.resume();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain); gain.connect(ctx.destination);
      const now = ctx.currentTime;
      if (type === "absorb") {
        osc.type = "sine";
        osc.frequency.setValueAtTime(400, now); osc.frequency.exponentialRampToValueAtTime(800, now + 0.1);
        gain.gain.setValueAtTime(0.1, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
        osc.start(now); osc.stop(now + 0.1);
      } else if (type === "mutagen") {
        osc.type = "triangle";
        osc.frequency.setValueAtTime(600, now); osc.frequency.exponentialRampToValueAtTime(1200, now + 0.2);
        gain.gain.setValueAtTime(0.15, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
        osc.start(now); osc.stop(now + 0.2);
      } else if (type === "hit") {
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(150, now); osc.frequency.exponentialRampToValueAtTime(40, now + 0.25);
        gain.gain.setValueAtTime(0.25, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
        osc.start(now); osc.stop(now + 0.25);
      } else {
        osc.type = "sine";
        osc.frequency.setValueAtTime(300, now); osc.frequency.exponentialRampToValueAtTime(1500, now + 0.5);
        gain.gain.setValueAtTime(0.2, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
        osc.start(now); osc.stop(now + 0.5);
      }
    } catch (e) { console.error(e); }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setStats((prev) => {
        const colonizedCount = planets.filter((p) => p.status !== "Unexplored").length;
        const housingCount = tribalStructures.find((s) => s.id === "S1")?.count || 0;
        const sanctumCount = tribalStructures.find((s) => s.id === "S2")?.count || 0;
        const smelterCount = tribalStructures.find((s) => s.id === "S3")?.count || 0;
        const shrineCount = tribalStructures.find((s) => s.id === "S4")?.count || 0;
        return {
          ...prev,
          population: prev.population + housingCount * 5,
          dna: prev.dna + colonizedCount * 2 + sanctumCount * 3,
          starlight: prev.starlight + colonizedCount * 5,
          readiness: Math.min(100, prev.readiness + sanctumCount * 2),
          ecology: Math.min(100, Math.max(0, prev.ecology + shrineCount * 2 - smelterCount * 2)),
          industry: Math.min(100, Math.max(0, prev.industry + smelterCount * 3)),
        };
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [planets, tribalStructures]);

  const handleEvolveStat = (statName: keyof OrganismStats, cost: number) => {
    if (stats.dna < cost) return;
    playSound("mutagen");
    setStats((prev) => ({ ...prev, dna: prev.dna - cost, [statName]: (Number(prev[statName]) || 0) + 1 }));
    setLogs((prev) => [`[MUTATION SUCCESS] Evolved ${String(statName).toUpperCase()} attribute!`, ...prev.slice(0, 4)]);
  };

  const handleBuildTribalStructure = (struct: TribalStructure) => {
    if (stats.dna < struct.cost) return;
    playSound("build");
    setStats((prev) => ({ ...prev, dna: prev.dna - struct.cost }));
    setTribalStructures((prev) => prev.map((s) => (s.id === struct.id ? { ...s, count: s.count + 1 } : s)));
    setLogs((prev) => [`[TRIBAL CONSTRUCT] Built 1x ${struct.name}!`, ...prev.slice(0, 4)]);
  };

  const handleRegenerateHp = () => {
    if (stats.dna < 15 || stats.hp >= stats.maxHp) return;
    playSound("absorb");
    setStats((prev) => ({ ...prev, dna: prev.dna - 15, hp: Math.min(prev.maxHp, prev.hp + 35) }));
    setLogs((prev) => [`[CELL REPAIR] Regenerated Cellular Integrity (+35 HP)`, ...prev.slice(0, 4)]);
  };

  const handleAscendEra = () => {
    if (stats.readiness < 100) return;
    playSound("ascend");
    const nextStage = stats.stage === "Cellular" ? "Aquatic" : stats.stage === "Aquatic" ? "Tribal" : "Galactic";
    setStats((prev) => ({ ...prev, stage: nextStage, readiness: 0, maxHp: prev.maxHp + 50, hp: prev.maxHp + 50 }));
    if (nextStage === "Tribal") setActiveViewMode("Tribal");
    if (nextStage === "Galactic") setActiveViewMode("GalacticMap");
    setLogs((prev) => [`[EVOLUTION ASCENSION] Species ascended to the ${nextStage.toUpperCase()} Era!`, ...prev.slice(0, 4)]);
  };

  const handleColonizePlanet = (planet: PlanetNode) => {
    if (stats.dna < planet.cost || planet.status !== "Unexplored") return;
    playSound("ascend");
    setStats((prev) => ({ ...prev, dna: prev.dna - planet.cost }));
    setPlanets((prev) => prev.map((p) => (p.id === planet.id ? { ...p, status: "Colonized", population: 100000 } : p)));
    setSelectedPlanet((prev) => (prev.id === planet.id ? { ...prev, status: "Colonized", population: 100000 } : prev));
    setLogs((prev) => [`[COLONIZATION SUCCESS] Established outpost on ${planet.name}!`, ...prev.slice(0, 4)]);
  };

  const MODE_LABELS: Record<string, string> = {
    Cellular: "CELLULAR POOL", Tribal: "TRIBAL SPHERE", GalacticMap: "GALACTIC MAP",
  };
  const MODE_ACTIVE_CLASSES: Record<string, string> = {
    Cellular: "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold",
    Tribal: "bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold",
    GalacticMap: "bg-purple-500/20 text-purple-300 border border-purple-500/40 font-bold",
  };
  const UPGRADES = [
    { name: "speed", label: "Flagella Propulsion (Speed)", val: stats.speed, cost: 20, desc: "Outrun Predator ICES in fluid" },
    { name: "armor", label: "Chitin Membrane (Armor)", val: stats.armor, cost: 30, desc: "Reduces ICES & Toxic Acid damage" },
    { name: "ingestion", label: "Cytostome (Ingestion)", val: stats.ingestion, cost: 25, desc: "Multiplies DNA gained per nutrient" },
    { name: "intelligence", label: "Neural Ganglia (Intellect)", val: stats.intelligence, cost: 40, desc: "Unlocks advanced tribal tech" },
  ];

  return (
    <div className="space-y-6 animate-appear font-mono">
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div>
          <h2 className="text-sm font-bold tracking-[0.25em] text-white uppercase flex items-center gap-2">
            <span>NEO-GENESIS EVOLUTION</span>
            <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded border border-cyan-500/30 font-mono">EVOLUTIONARY SIMULATOR</span>
          </h2>
          <p className="text-[11px] text-white/40 font-mono mt-0.5">Nurture your organism through biological mutations and build planetary civilizations</p>
        </div>
        <div className="flex items-center gap-3 font-mono">
          <button
            onClick={() => setAudioEnabled(!audioEnabled)}
            className={`px-3 py-1.5 min-h-[44px] text-xs rounded border transition-all cursor-pointer flex items-center gap-1.5 ${audioEnabled ? "bg-green-500/20 text-green-300 border-green-500/40" : "bg-white/5 text-white/40 border-white/10"}`}
          >
            {audioEnabled ? "SYNTH AUDIO: ON" : "AUDIO: MUTED"}
          </button>
          <div className="flex items-center bg-deep-space border border-white/10 rounded p-1">
            {(["Cellular", "Tribal", "GalacticMap"] as const).map((mode) => (
              <button key={mode} onClick={() => setActiveViewMode(mode)}
                className={`px-3 py-1.5 min-h-[44px] text-xs rounded transition-all cursor-pointer ${activeViewMode === mode ? MODE_ACTIVE_CLASSES[mode] : "text-white/50 hover:text-white"}`}
              >
                {MODE_LABELS[mode]}
              </button>
            ))}
          </div>
          <div className="text-right font-mono text-[10px] text-white/40 border-l border-white/10 pl-3">
            Current Era: <span className="text-cyan-400 font-bold uppercase">{stats.stage}</span>
          </div>
        </div>
      </div>

      {activeViewMode === "Cellular" ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-7 space-y-4">
            <div className="bg-panel-bg/40 border border-cyan-500/30 p-4 rounded-xl space-y-3 shadow-2xl backdrop-blur-md">
              <div className="flex justify-between items-center text-xs border-b border-white/10 pb-2">
                <span className="text-cyan-400 font-bold flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
                  STAGE I: PRIMORDIAL FLUID & HAZARD ZONES
                </span>
                <span className="text-[10px] text-white/40">W/A/S/D or Arrow Keys to move</span>
              </div>
              <CellularCanvas stats={stats} setStats={setStats} audioEnabled={audioEnabled} playSound={playSound} setLogs={setLogs} />
              <div className="bg-deep-space p-3 rounded-lg border border-white/5 space-y-1 text-[11px] text-white/70">
                <span className="text-[10px] text-white/30 uppercase block font-semibold mb-1">Biological Event Feed</span>
                {logs.map((log, idx) => (
                  <p key={idx} className={idx === 0 ? "text-cyan-300 font-semibold" : "text-white/50"}>{log}</p>
                ))}
              </div>
            </div>
          </div>

          <div className="lg:col-span-5 space-y-4">
            <div className="bg-panel-bg/40 border border-purple-500/30 p-5 rounded-xl space-y-5 shadow-2xl backdrop-blur-md">
              <div className="flex justify-between items-center border-b border-white/10 pb-3">
                <div>
                  <h3 className="text-xs font-bold text-purple-400 uppercase tracking-wider">DNA MUTATION CHAMBER</h3>
                  <p className="text-[10px] text-white/40">Evolve armor & traits to survive predators</p>
                </div>
                <div className="text-right">
                  <span className="text-[10px] text-white/40 uppercase block">Available DNA</span>
                  <span className="text-xl font-bold text-amber-400">{stats.dna}</span>
                </div>
              </div>
              <div className="space-y-1.5 bg-deep-space p-3 rounded-lg border border-white/5">
                <div className="flex justify-between text-[11px]">
                  <span className="text-white/60">ORGANISM INTEGRITY (HP)</span>
                  <span className={`font-bold ${stats.hp < 30 ? "text-red-400 animate-pulse" : "text-green-400"}`}>{stats.hp} / {stats.maxHp}</span>
                </div>
                <div className="w-full h-2.5 bg-black/60 rounded-full overflow-hidden border border-white/10 p-0.5">
                  <div className={`h-full rounded-full transition-all duration-300 ${stats.hp < 30 ? "bg-red-500" : "bg-green-400"}`} style={{ width: `${(stats.hp / stats.maxHp) * 100}%` }} />
                </div>
                {stats.hp < stats.maxHp && (
                  <button onClick={handleRegenerateHp} disabled={stats.dna < 15}
                    className="w-full mt-2 py-1.5 min-h-[44px] bg-green-500/15 hover:bg-green-500/30 border border-green-500/40 text-green-300 rounded text-xs font-semibold disabled:opacity-30 disabled:cursor-not-allowed transition-all cursor-pointer"
                  >
                    REGENERATE INTEGRITY (15 DNA)
                  </button>
                )}
              </div>
              <div className="space-y-1.5">
                <div className="flex justify-between text-[11px]">
                  <span className="text-white/60">EVOLUTION READINESS</span>
                  <span className="text-cyan-400 font-bold">{stats.readiness}%</span>
                </div>
                <div className="w-full h-2.5 bg-deep-space rounded-full overflow-hidden border border-white/10 p-0.5">
                  <div className="h-full bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full transition-all duration-300" style={{ width: `${stats.readiness}%` }} />
                </div>
                {stats.readiness >= 100 && (
                  <button onClick={handleAscendEra}
                    className="w-full min-h-[44px] mt-2 py-2 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 hover:from-cyan-500/40 hover:to-purple-500/40 border border-cyan-400 text-cyan-300 rounded-lg text-xs font-bold tracking-widest uppercase transition-all shadow-lg animate-pulse cursor-pointer"
                  >
                    ASCEND TO {stats.stage === "Cellular" ? "AQUATIC" : stats.stage === "Aquatic" ? "TRIBAL" : "GALACTIC"} ERA
                  </button>
                )}
              </div>
              <div className="space-y-2.5 pt-1">
                <h4 className="text-[10px] text-white/40 uppercase tracking-wider font-semibold">Biological Upgrades</h4>
                {UPGRADES.map((up) => (
                  <div key={up.name} className="bg-deep-space p-3 rounded-lg border border-white/5 flex justify-between items-center">
                    <div>
                      <span className="text-xs font-bold text-white/90 block">{up.label}</span>
                      <span className="text-[10px] text-white/40 block">{up.desc} (Lvl {up.val})</span>
                    </div>
                    <button onClick={() => handleEvolveStat(up.name as keyof OrganismStats, up.cost)} disabled={stats.dna < up.cost}
                      className="px-3 py-1.5 min-h-[44px] bg-purple-500/15 hover:bg-purple-500/30 border border-purple-500/40 text-purple-300 rounded text-xs font-semibold disabled:opacity-30 disabled:cursor-not-allowed transition-all cursor-pointer flex flex-col items-center justify-center"
                    >
                      <span>EVOLVE</span>
                      <span className="text-[9px] text-amber-400 font-mono">{up.cost} DNA</span>
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      ) : activeViewMode === "Tribal" ? (
        <TribalManagement stats={stats} tribalStructures={tribalStructures} logs={logs} onBuildStructure={handleBuildTribalStructure} />
      ) : (
        <GalacticMap stats={stats} planets={planets} selectedPlanet={selectedPlanet} onSelectPlanet={setSelectedPlanet} onColonizePlanet={handleColonizePlanet} />
      )}
    </div>
  );
};
