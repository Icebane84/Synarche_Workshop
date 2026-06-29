import React, { useState, useEffect, useRef } from "react";
import { NexusSignalBusClient } from "@synarche/nexus-signalbus";

interface OrganismStats {
  hp: number;
  maxHp: number;
  dna: number;
  starlight: number;
  population: number;
  ecology: number;
  industry: number;
  stage: "Cellular" | "Aquatic" | "Tribal" | "Galactic";
  speed: number;
  armor: number;
  ingestion: number;
  intelligence: number;
  readiness: number;
}

interface Nutrient {
  x: number;
  y: number;
  size: number;
  color: string;
  type: "amino" | "lipid" | "mutagen";
}

interface PredatorICE {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  name: string;
}

interface ToxicZone {
  x: number;
  y: number;
  radius: number;
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  color: string;
  life: number;
  maxLife: number;
  size: number;
}

interface TribalStructure {
  id: string;
  name: string;
  type: string;
  cost: number;
  count: number;
  effect: string;
  icon: string;
}

interface PlanetNode {
  id: string;
  name: string;
  type: string;
  color: string;
  cost: number;
  status: "Unexplored" | "Colonized" | "Terraformed";
  population: number;
  output: string;
}

const INITIAL_PLANETS: PlanetNode[] = [
  { id: "P1", name: "Solaria Prime", type: "Terran Origin World", color: "text-cyan-400 border-cyan-500/40 bg-cyan-500/10", cost: 0, status: "Colonized", population: 2500000, output: "+50 DNA/sec" },
  { id: "P2", name: "Kryon-9", type: "Glacial Cryo-World", color: "text-blue-400 border-blue-500/40 bg-blue-500/10", cost: 150, status: "Unexplored", population: 0, output: "+100 Mutagens/sec" },
  { id: "P3", name: "Aetheria IV", type: "Gas Giant Dyson Station", color: "text-purple-400 border-purple-500/40 bg-purple-500/10", cost: 300, status: "Unexplored", population: 0, output: "+200 Starlight/sec" },
  { id: "P4", name: "Vulcanus Prime", type: "Magma Core Mining Sphere", color: "text-amber-400 border-amber-500/40 bg-amber-500/10", cost: 500, status: "Unexplored", population: 0, output: "+400 Industry/sec" },
  { id: "P5", name: "Zephyr Alpha", type: "Hyper-Biosphere Reserve", color: "text-green-400 border-green-500/40 bg-green-500/10", cost: 800, status: "Unexplored", population: 0, output: "+1000 DNA/sec" },
];

const INITIAL_TRIBAL_STRUCTURES: TribalStructure[] = [
  { id: "S1", name: "Bio-Habitat Pod", type: "HOUSING", cost: 40, count: 2, effect: "+25 Pop Growth/sec", icon: "🛖" },
  { id: "S2", name: "Spore Sanctum", type: "CULTURE", cost: 60, count: 1, effect: "+5 DNA & Readiness/sec", icon: "🔮" },
  { id: "S3", name: "Chitin Smelter", type: "INDUSTRY", cost: 80, count: 0, effect: "+15 Industry, -5% Ecology", icon: "🏭" },
  { id: "S4", name: "Ecology Shrine", type: "ECO", cost: 75, count: 1, effect: "+10% Ecology Harmony", icon: "🌿" },
];

export const NeoGenesisGame: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [stats, setStats] = useState<OrganismStats>({
    hp: 100,
    maxHp: 100,
    dna: 20,
    starlight: 50,
    population: 120,
    ecology: 85,
    industry: 15,
    stage: "Cellular",
    speed: 2,
    armor: 1,
    ingestion: 1,
    intelligence: 1,
    readiness: 0,
  });

  const [activeViewMode, setActiveViewMode] = useState<"Cellular" | "Tribal" | "GalacticMap">("Cellular");
  const [tribalStructures, setTribalStructures] = useState<TribalStructure[]>(INITIAL_TRIBAL_STRUCTURES);
  const [planets, setPlanets] = useState<PlanetNode[]>(INITIAL_PLANETS);
  const [selectedPlanet, setSelectedPlanet] = useState<PlanetNode>(INITIAL_PLANETS[0]);
  const [audioEnabled, setAudioEnabled] = useState(false);

  const [logs, setLogs] = useState<string[]>([
    "Standalone Neo-Genesis engine initialized. Beware of Predator ICES & Toxic Acid Biomes!",
  ]);

  const playerRef = useRef({ x: 300, y: 200, radius: 14, color: "#00f0ff" });
  const nutrientsRef = useRef<Nutrient[]>([]);
  const predatorsRef = useRef<PredatorICE[]>([]);
  const toxicZonesRef = useRef<ToxicZone[]>([]);
  const particlesRef = useRef<Particle[]>([]);
  const shakeRef = useRef<number>(0);
  const keysRef = useRef<{ [key: string]: boolean }>({});
  const lastDamageTimeRef = useRef<number>(0);
  const audioCtxRef = useRef<AudioContext | null>(null);
  const busRef = useRef<NexusSignalBusClient | null>(null);

  useEffect(() => {
    busRef.current = new NexusSignalBusClient("neo-genesis");
    return () => {
      busRef.current?.close();
    };
  }, []);

  const playSound = (type: "absorb" | "mutagen" | "hit" | "ascend" | "build") => {
    if (!audioEnabled) return;
    try {
      if (!audioCtxRef.current) {
        audioCtxRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
      }
      const ctx = audioCtxRef.current;
      if (ctx.state === "suspended") ctx.resume();

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);

      const now = ctx.currentTime;
      if (type === "absorb") {
        osc.type = "sine";
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.exponentialRampToValueAtTime(800, now + 0.1);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
        osc.start(now);
        osc.stop(now + 0.1);
      } else if (type === "mutagen") {
        osc.type = "triangle";
        osc.frequency.setValueAtTime(600, now);
        osc.frequency.exponentialRampToValueAtTime(1200, now + 0.2);
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
        osc.start(now);
        osc.stop(now + 0.2);
      } else if (type === "hit") {
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.exponentialRampToValueAtTime(40, now + 0.25);
        gain.gain.setValueAtTime(0.25, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
        osc.start(now);
        osc.stop(now + 0.25);
      } else if (type === "ascend" || type === "build") {
        osc.type = "sine";
        osc.frequency.setValueAtTime(300, now);
        osc.frequency.exponentialRampToValueAtTime(1500, now + 0.5);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
        osc.start(now);
        osc.stop(now + 0.5);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const spawnParticleSparks = (x: number, y: number, color: string, count = 12) => {
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 4 + 1;
      particlesRef.current.push({
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        color,
        life: 0,
        maxLife: Math.random() * 20 + 15,
        size: Math.random() * 3 + 2,
      });
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setStats((prev) => {
        const colonizedCount = planets.filter((p) => p.status !== "Unexplored").length;
        const housingCount = tribalStructures.find((s) => s.id === "S1")?.count || 0;
        const sanctumCount = tribalStructures.find((s) => s.id === "S2")?.count || 0;
        const smelterCount = tribalStructures.find((s) => s.id === "S3")?.count || 0;
        const shrineCount = tribalStructures.find((s) => s.id === "S4")?.count || 0;

        const popGain = housingCount * 5;
        const dnaGain = colonizedCount * 2 + sanctumCount * 3;
        const starlightGain = colonizedCount * 5;
        const readinessGain = sanctumCount * 2;

        const newEcology = Math.min(100, Math.max(0, prev.ecology + shrineCount * 2 - smelterCount * 2));
        const newIndustry = Math.min(100, Math.max(0, prev.industry + smelterCount * 3));

        return {
          ...prev,
          population: prev.population + popGain,
          dna: prev.dna + dnaGain,
          starlight: prev.starlight + starlightGain,
          readiness: Math.min(100, prev.readiness + readinessGain),
          ecology: newEcology,
          industry: newIndustry,
        };
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [planets, tribalStructures]);

  useEffect(() => {
    const nutArr: Nutrient[] = [];
    for (let i = 0; i < 25; i++) {
      nutArr.push({
        x: Math.random() * 600,
        y: Math.random() * 400,
        size: Math.random() * 4 + 3,
        color: Math.random() > 0.3 ? "#00f0ff" : Math.random() > 0.5 ? "#a855f7" : "#f59e0b",
        type: Math.random() > 0.3 ? "amino" : Math.random() > 0.5 ? "lipid" : "mutagen",
      });
    }
    nutrientsRef.current = nutArr;

    predatorsRef.current = [
      { x: 100, y: 100, vx: 1.2, vy: 0.8, radius: 18, name: "ICE-PHANTOM-01" },
      { x: 500, y: 300, vx: -1.0, vy: 1.5, radius: 20, name: "ICE-APEX-02" },
    ];

    toxicZonesRef.current = [
      { x: 150, y: 280, radius: 55 },
      { x: 450, y: 120, radius: 65 },
    ];
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => { keysRef.current[e.key] = true; };
    const handleKeyUp = (e: KeyboardEvent) => { keysRef.current[e.key] = false; };
    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  useEffect(() => {
    if (activeViewMode !== "Cellular") return;
    let animationFrameId: number;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const render = () => {
      const now = Date.now();

      const moveSpeed = stats.speed * 1.5;
      const p = playerRef.current;
      if (keysRef.current["ArrowUp"] || keysRef.current["w"] || keysRef.current["W"]) p.y = Math.max(p.radius, p.y - moveSpeed);
      if (keysRef.current["ArrowDown"] || keysRef.current["s"] || keysRef.current["S"]) p.y = Math.min(canvas.height - p.radius, p.y + moveSpeed);
      if (keysRef.current["ArrowLeft"] || keysRef.current["a"] || keysRef.current["A"]) p.x = Math.max(p.radius, p.x - moveSpeed);
      if (keysRef.current["ArrowRight"] || keysRef.current["d"] || keysRef.current["D"]) p.x = Math.min(canvas.width - p.radius, p.x + moveSpeed);

      ctx.save();
      if (shakeRef.current > 0) {
        const dx = (Math.random() - 0.5) * shakeRef.current;
        const dy = (Math.random() - 0.5) * shakeRef.current;
        ctx.translate(dx, dy);
        shakeRef.current *= 0.85;
        if (shakeRef.current < 0.5) shakeRef.current = 0;
      }

      ctx.fillStyle = "#090a0f";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.strokeStyle = "rgba(0, 240, 255, 0.05)";
      ctx.lineWidth = 1;
      for (let x = 0; x < canvas.width; x += 30) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke(); }
      for (let y = 0; y < canvas.height; y += 30) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke(); }

      toxicZonesRef.current.forEach((z) => {
        ctx.beginPath();
        ctx.arc(z.x, z.y, z.radius, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(239, 68, 68, 0.15)";
        ctx.strokeStyle = "rgba(239, 68, 68, 0.4)";
        ctx.lineWidth = 2;
        ctx.shadowColor = "#ef4444";
        ctx.shadowBlur = 15;
        ctx.fill();
        ctx.stroke();
        ctx.shadowBlur = 0;

        const dist = Math.hypot(p.x - z.x, p.y - z.y);
        if (dist < z.radius + p.radius) {
          if (now - lastDamageTimeRef.current > 400) {
            lastDamageTimeRef.current = now;
            shakeRef.current = 8;
            playSound("hit");
            spawnParticleSparks(p.x, p.y, "#ef4444", 8);
            const dmg = Math.max(2, 8 - stats.armor * 2);
            setStats((prev) => ({ ...prev, hp: Math.max(0, prev.hp - dmg) }));
            setLogs((prev) => [`[HAZARD WARN] Toxic Acid corrosion! Armor absorbed part of damage (-${dmg} HP)`, ...prev.slice(0, 4)]);
          }
        }
      });

      nutrientsRef.current.forEach((n) => {
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.size, 0, Math.PI * 2);
        ctx.fillStyle = n.color;
        ctx.shadowColor = n.color;
        ctx.shadowBlur = 8;
        ctx.fill();
        ctx.shadowBlur = 0;

        const dist = Math.hypot(p.x - n.x, p.y - n.y);
        if (dist < p.radius + n.size) {
          spawnParticleSparks(n.x, n.y, n.color, n.type === "mutagen" ? 18 : 10);
          if (n.type === "mutagen") {
            shakeRef.current = 6;
            playSound("mutagen");
          } else {
            playSound("absorb");
          }

          n.x = Math.random() * canvas.width;
          n.y = Math.random() * canvas.height;
          const dnaGained = n.type === "mutagen" ? 6 : 3;
          setStats((prev) => {
            const newDna = prev.dna + dnaGained * prev.ingestion;
            const newReadiness = Math.min(100, prev.readiness + 2);
            const newHp = Math.min(prev.maxHp, prev.hp + 1);
            return { ...prev, dna: newDna, readiness: newReadiness, hp: newHp };
          });
        }
      });

      predatorsRef.current.forEach((pred) => {
        pred.x += pred.vx;
        pred.y += pred.vy;

        if (pred.x <= pred.radius || pred.x >= canvas.width - pred.radius) pred.vx *= -1;
        if (pred.y <= pred.radius || pred.y >= canvas.height - pred.radius) pred.vy *= -1;

        ctx.beginPath();
        ctx.arc(pred.x, pred.y, pred.radius, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(255, 0, 85, 0.3)";
        ctx.strokeStyle = "#ff0055";
        ctx.lineWidth = 3;
        ctx.shadowColor = "#ff0055";
        ctx.shadowBlur = 16;
        ctx.fill();
        ctx.stroke();
        ctx.shadowBlur = 0;

        ctx.beginPath();
        ctx.arc(pred.x, pred.y, pred.radius * 0.4, 0, Math.PI * 2);
        ctx.fillStyle = "#ff0055";
        ctx.fill();

        const dist = Math.hypot(p.x - pred.x, p.y - pred.y);
        if (dist < p.radius + pred.radius) {
          if (now - lastDamageTimeRef.current > 600) {
            lastDamageTimeRef.current = now;
            shakeRef.current = 16;
            playSound("hit");
            spawnParticleSparks(p.x, p.y, "#ff0055", 20);
            const dmg = Math.max(5, 20 - stats.armor * 4);
            setStats((prev) => ({ ...prev, hp: Math.max(0, prev.hp - dmg) }));
            setLogs((prev) => [`🚨 [ICE AMBUSH] ${pred.name} struck organism! (-${dmg} HP)`, ...prev.slice(0, 4)]);
          }
        }
      });

      particlesRef.current.forEach((pt) => {
        pt.x += pt.vx;
        pt.y += pt.vy;
        pt.life++;

        const alpha = Math.max(0, 1 - pt.life / pt.maxLife);
        const currentRadius = Math.max(0.1, pt.size * alpha);
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, currentRadius, 0, Math.PI * 2);
        ctx.fillStyle = pt.color;
        ctx.globalAlpha = alpha;
        ctx.fill();
        ctx.globalAlpha = 1.0;
      });
      particlesRef.current = particlesRef.current.filter((pt) => pt.life < pt.maxLife);

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(0, 240, 255, 0.25)";
      ctx.strokeStyle = stats.hp < 30 ? "#ef4444" : "#00f0ff";
      ctx.lineWidth = 2.5;
      ctx.shadowColor = stats.hp < 30 ? "#ef4444" : "#00f0ff";
      ctx.shadowBlur = 14;
      ctx.fill();
      ctx.stroke();
      ctx.shadowBlur = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius * 0.45, 0, Math.PI * 2);
      ctx.fillStyle = "#a855f7";
      ctx.fill();

      ctx.restore();
      animationFrameId = requestAnimationFrame(render);
    };

    render();
    return () => cancelAnimationFrame(animationFrameId);
  }, [stats.speed, stats.ingestion, stats.armor, activeViewMode, audioEnabled]);

  const handleEvolveStat = (statName: keyof OrganismStats, cost: number) => {
    if (stats.dna < cost) return;
    playSound("mutagen");
    setStats((prev) => ({
      ...prev,
      dna: prev.dna - cost,
      [statName]: (Number(prev[statName]) || 0) + 1,
    }));
    setLogs((prev) => [
      `[MUTATION SUCCESS] Evolved ${String(statName).toUpperCase()} attribute!`,
      ...prev.slice(0, 4),
    ]);
  };

  const handleBuildTribalStructure = (struct: TribalStructure) => {
    if (stats.dna < struct.cost) return;
    playSound("build");
    setStats((prev) => ({ ...prev, dna: prev.dna - struct.cost }));
    setTribalStructures((prev) =>
      prev.map((s) => (s.id === struct.id ? { ...s, count: s.count + 1 } : s))
    );
    setLogs((prev) => [`🏗️ [TRIBAL CONSTRUCT] Built 1x ${struct.name}!`, ...prev.slice(0, 4)]);
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
    const nextStage =
      stats.stage === "Cellular" ? "Aquatic" : stats.stage === "Aquatic" ? "Tribal" : "Galactic";
    setStats((prev) => ({ ...prev, stage: nextStage, readiness: 0, maxHp: prev.maxHp + 50, hp: prev.maxHp + 50 }));
    if (nextStage === "Tribal") setActiveViewMode("Tribal");
    if (nextStage === "Galactic") setActiveViewMode("GalacticMap");
    setLogs((prev) => [
      `🌟 [EVOLUTION ASCENSION] Species ascended to the ${nextStage.toUpperCase()} Era!`,
      ...prev.slice(0, 4),
    ]);

    busRef.current?.emit("GAME_EVENT", "ASCEND_ERA", {
      nextStage,
      dna: stats.dna,
      population: stats.population,
    });
  };

  const handleColonizePlanet = (planet: PlanetNode) => {
    if (stats.dna < planet.cost || planet.status !== "Unexplored") return;
    playSound("ascend");
    setStats((prev) => ({ ...prev, dna: prev.dna - planet.cost }));
    setPlanets((prev) =>
      prev.map((p) => (p.id === planet.id ? { ...p, status: "Colonized", population: 100000 } : p))
    );
    setSelectedPlanet((prev) => (prev.id === planet.id ? { ...prev, status: "Colonized", population: 100000 } : prev));
    setLogs((prev) => [`🚀 [COLONIZATION SUCCESS] Established outpost on ${planet.name}!`, ...prev.slice(0, 4)]);

    busRef.current?.emit("GAME_EVENT", "COLONIZE_PLANET", {
      planetName: planet.name,
      planetType: planet.type,
    });
  };

  return (
    <div className="min-h-screen bg-[#090a0f] text-white p-6 space-y-6 font-mono">
      {/* View Header */}
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div>
          <h2 className="text-sm font-bold tracking-[0.25em] text-white uppercase flex items-center gap-2">
            <span>NEO-GENESIS EVOLUTION</span>
            <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded border border-cyan-500/30 font-mono">
              STANDALONE ENGINE V1.0
            </span>
          </h2>
          <p className="text-[11px] text-white/40 font-mono mt-0.5">
            Nurture your organism through biological mutations and build planetary civilizations
          </p>
        </div>
        <div className="flex items-center gap-3 font-mono">
          <button
            onClick={() => setAudioEnabled(!audioEnabled)}
            className={`px-3 py-1.5 min-h-[44px] text-xs rounded border transition-all cursor-pointer flex items-center gap-1.5 ${
              audioEnabled ? "bg-green-500/20 text-green-300 border-green-500/40" : "bg-white/5 text-white/40 border-white/10"
            }`}
          >
            <span>{audioEnabled ? "🔊 SYNTH AUDIO: ON" : "🔇 AUDIO: MUTED"}</span>
          </button>

          <div className="flex items-center bg-[#0d0f17] border border-white/10 rounded p-1">
            <button
              onClick={() => setActiveViewMode("Cellular")}
              className={`px-3 py-1.5 min-h-[44px] text-xs rounded transition-all cursor-pointer ${
                activeViewMode === "Cellular" ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold" : "text-white/50 hover:text-white"
              }`}
            >
              🔬 CELLULAR POOL
            </button>
            <button
              onClick={() => setActiveViewMode("Tribal")}
              className={`px-3 py-1.5 min-h-[44px] text-xs rounded transition-all cursor-pointer ${
                activeViewMode === "Tribal" ? "bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold" : "text-white/50 hover:text-white"
              }`}
            >
              🏛️ TRIBAL SPHERE
            </button>
            <button
              onClick={() => setActiveViewMode("GalacticMap")}
              className={`px-3 py-1.5 min-h-[44px] text-xs rounded transition-all cursor-pointer ${
                activeViewMode === "GalacticMap" ? "bg-purple-500/20 text-purple-300 border border-purple-500/40 font-bold" : "text-white/50 hover:text-white"
              }`}
            >
              🌌 GALACTIC MAP
            </button>
          </div>
          <div className="text-right font-mono text-[10px] text-white/40 border-l border-white/10 pl-3">
            Current Era: <span className="text-cyan-400 font-bold uppercase">{stats.stage}</span>
          </div>
        </div>
      </div>

      {/* View Mode Switcher */}
      {activeViewMode === "Cellular" ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-7 space-y-4">
            <div className="bg-[#121520]/60 border border-cyan-500/30 p-4 rounded-xl space-y-3 shadow-2xl backdrop-blur-md relative overflow-hidden">
              <div className="flex justify-between items-center text-xs border-b border-white/10 pb-2">
                <span className="text-cyan-400 font-bold flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
                  STAGE I: PRIMORDIAL FLUID & HAZARD ZONES
                </span>
                <span className="text-[10px] text-white/40">W/A/S/D or Arrow Keys to move</span>
              </div>

              <div className="relative flex justify-center bg-black/60 rounded-lg overflow-hidden border border-white/10">
                <canvas ref={canvasRef} width={600} height={400} className="w-full h-auto max-h-[400px] cursor-crosshair" />
              </div>

              <div className="bg-[#0d0f17] p-3 rounded-lg border border-white/5 space-y-1 text-[11px] text-white/70">
                <span className="text-[10px] text-white/30 uppercase block font-semibold mb-1">Biological Event Feed</span>
                {logs.map((log, idx) => (
                  <p key={idx} className={idx === 0 ? "text-cyan-300 font-semibold" : "text-white/50"}>
                    {log}
                  </p>
                ))}
              </div>
            </div>
          </div>

          <div className="lg:col-span-5 space-y-4">
            <div className="bg-[#121520]/60 border border-purple-500/30 p-5 rounded-xl space-y-5 shadow-2xl backdrop-blur-md">
              <div className="flex justify-between items-center border-b border-white/10 pb-3">
                <div>
                  <h3 className="text-xs font-bold text-purple-400 uppercase tracking-wider">🧬 DNA MUTATION CHAMBER</h3>
                  <p className="text-[10px] text-white/40">Evolve armor & traits to survive predators</p>
                </div>
                <div className="text-right">
                  <span className="text-[10px] text-white/40 uppercase block">Available DNA</span>
                  <span className="text-xl font-bold text-amber-400">{stats.dna}</span>
                </div>
              </div>

              <div className="space-y-1.5 bg-[#0d0f17] p-3 rounded-lg border border-white/5">
                <div className="flex justify-between text-[11px]">
                  <span className="text-white/60">ORGANISM INTEGRITY (HP)</span>
                  <span className={`font-bold ${stats.hp < 30 ? "text-red-400 animate-pulse" : "text-green-400"}`}>
                    {stats.hp} / {stats.maxHp}
                  </span>
                </div>
                <div className="w-full h-2.5 bg-black/60 rounded-full overflow-hidden border border-white/10 p-0.5">
                  <div className={`h-full rounded-full transition-all duration-300 ${stats.hp < 30 ? "bg-red-500" : "bg-green-400"}`} style={{ width: `${(stats.hp / stats.maxHp) * 100}%` }} />
                </div>
                {stats.hp < stats.maxHp && (
                  <button
                    onClick={handleRegenerateHp}
                    disabled={stats.dna < 15}
                    className="w-full mt-2 py-1.5 min-h-[44px] bg-green-500/15 hover:bg-green-500/30 border border-green-500/40 text-green-300 rounded text-xs font-semibold disabled:opacity-30 disabled:cursor-not-allowed transition-all cursor-pointer"
                  >
                    🩹 REGENERATE INTEGRITY (15 DNA)
                  </button>
                )}
              </div>

              <div className="space-y-1.5">
                <div className="flex justify-between text-[11px]">
                  <span className="text-white/60">EVOLUTION READINESS</span>
                  <span className="text-cyan-400 font-bold">{stats.readiness}%</span>
                </div>
                <div className="w-full h-2.5 bg-[#0d0f17] rounded-full overflow-hidden border border-white/10 p-0.5">
                  <div className="h-full bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full transition-all duration-300" style={{ width: `${stats.readiness}%` }} />
                </div>
                {stats.readiness >= 100 && (
                  <button
                    onClick={handleAscendEra}
                    className="w-full min-h-[44px] mt-2 py-2 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 hover:from-cyan-500/40 hover:to-purple-500/40 border border-cyan-400 text-cyan-300 rounded-lg text-xs font-bold tracking-widest uppercase transition-all shadow-lg animate-pulse cursor-pointer"
                  >
                    🚀 ASCEND TO {stats.stage === "Cellular" ? "AQUATIC" : stats.stage === "Aquatic" ? "TRIBAL" : "GALACTIC"} ERA
                  </button>
                )}
              </div>

              <div className="space-y-2.5 pt-1">
                <h4 className="text-[10px] text-white/40 uppercase tracking-wider font-semibold">Biological Upgrades</h4>
                {[
                  { name: "speed", label: "Flagella Propulsion (Speed)", val: stats.speed, cost: 20, desc: "Outrun Predator ICES in fluid" },
                  { name: "armor", label: "Chitin Membrane (Armor)", val: stats.armor, cost: 30, desc: "Reduces ICES & Toxic Acid damage" },
                  { name: "ingestion", label: "Cytostome (Ingestion)", val: stats.ingestion, cost: 25, desc: "Multiplies DNA gained per nutrient" },
                  { name: "intelligence", label: "Neural Ganglia (Intellect)", val: stats.intelligence, cost: 40, desc: "Unlocks advanced tribal tech" },
                ].map((up) => (
                  <div key={up.name} className="bg-[#0d0f17] p-3 rounded-lg border border-white/5 flex justify-between items-center">
                    <div>
                      <span className="text-xs font-bold text-white/90 block">{up.label}</span>
                      <span className="text-[10px] text-white/40 block">{up.desc} (Lvl {up.val})</span>
                    </div>
                    <button
                      onClick={() => handleEvolveStat(up.name as keyof OrganismStats, up.cost)}
                      disabled={stats.dna < up.cost}
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
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 font-mono">
          <div className="lg:col-span-7 space-y-4">
            <div className="bg-[#121520]/60 border border-amber-500/40 p-5 rounded-xl space-y-5 shadow-2xl backdrop-blur-md">
              <div className="flex justify-between items-center border-b border-white/10 pb-3">
                <div>
                  <h3 className="text-xs font-bold text-amber-300 uppercase tracking-wider flex items-center gap-2">
                    <span>🏛️ STAGE II: TRIBAL HABITAT & TERRITORIAL MAP</span>
                  </h3>
                  <p className="text-[10px] text-white/40">Manage population growth and balance ecological harmony with industrial expansion</p>
                </div>
                <div className="text-right">
                  <span className="text-[10px] text-white/40 uppercase block">Tribal Population</span>
                  <span className="text-lg font-bold text-amber-400">👥 {stats.population.toLocaleString()}</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 bg-[#0d0f17] p-4 rounded-lg border border-white/5">
                <div className="space-y-1">
                  <div className="flex justify-between text-[11px]">
                    <span className="text-green-400 font-semibold">🌿 ECOLOGICAL HARMONY</span>
                    <span className="text-white font-bold">{stats.ecology}%</span>
                  </div>
                  <div className="w-full h-2 bg-black/60 rounded-full overflow-hidden border border-white/10">
                    <div className="h-full bg-green-500 transition-all duration-300" style={{ width: `${stats.ecology}%` }} />
                  </div>
                </div>

                <div className="space-y-1">
                  <div className="flex justify-between text-[11px]">
                    <span className="text-amber-400 font-semibold">⚙️ INDUSTRIAL OUTPUT</span>
                    <span className="text-white font-bold">{stats.industry}%</span>
                  </div>
                  <div className="w-full h-2 bg-black/60 rounded-full overflow-hidden border border-white/10">
                    <div className="h-full bg-amber-500 transition-all duration-300" style={{ width: `${stats.industry}%` }} />
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <h4 className="text-[10px] text-white/40 uppercase tracking-wider font-semibold">Tribal Habitat Constructs</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {tribalStructures.map((st) => (
                    <div key={st.id} className="bg-[#0d0f17] p-3.5 rounded-lg border border-white/5 space-y-2 flex flex-col justify-between">
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
                        onClick={() => handleBuildTribalStructure(st)}
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
            <div className="bg-[#121520]/60 border border-cyan-500/40 p-5 rounded-xl space-y-5 shadow-2xl backdrop-blur-md">
              <div className="flex justify-between items-center border-b border-white/10 pb-3">
                <div>
                  <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-wider">📜 TRIBAL CHRONICLE & GOVERNANCE</h3>
                  <p className="text-[10px] text-white/40">Sovereign Species Progression</p>
                </div>
                <span className="text-[10px] px-2 py-0.5 rounded bg-green-500/20 text-green-300 border border-green-500/30 font-mono font-bold">STAGE II</span>
              </div>

              <div className="space-y-3 text-xs">
                <div className="bg-[#0d0f17] p-3 rounded border border-white/5 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-white/50">Sovereign Intellect:</span>
                    <span className="text-cyan-400 font-bold">Level {stats.intelligence}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/50">Habitat Capacity:</span>
                    <span className="text-white/90 font-semibold">{((tribalStructures.find((s) => s.id === "S1")?.count || 0) * 1000).toLocaleString()} Units</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/50">Next Evolution Tier:</span>
                    <span className="text-purple-400 font-bold">Interstellar Starfarer</span>
                  </div>
                </div>

                <div className="bg-[#0d0f17] p-3 rounded-lg border border-white/5 space-y-1 text-[11px] text-white/70">
                  <span className="text-[10px] text-white/30 uppercase block font-semibold mb-1">Tribal Event Chronicle</span>
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
      ) : (
        /* STAGE III: GALACTIC MAP */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-7 space-y-4">
            <div className="bg-[#121520]/60 border border-purple-500/40 p-5 rounded-xl space-y-4 shadow-2xl backdrop-blur-md">
              <div className="flex justify-between items-center border-b border-white/10 pb-3">
                <div>
                  <h3 className="text-xs font-bold text-purple-300 uppercase tracking-wider flex items-center gap-2">
                    <span>🌌 GALACTIC EXOPLANET STAR CHART</span>
                  </h3>
                  <p className="text-[10px] text-white/40">Dispatch interstellar colony ships to expand your species across star systems</p>
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
                      onClick={() => setSelectedPlanet(p)}
                      className={`p-4 rounded-lg border transition-all duration-200 cursor-pointer flex items-center justify-between ${
                        isSelected ? `${p.color} shadow-lg scale-[1.01]` : "bg-[#0d0f17]/60 border-white/5 hover:border-white/20"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`w-10 h-10 rounded-full border ${p.color} flex items-center justify-center font-bold text-sm shadow-inner`}>
                          🪐
                        </div>
                        <div>
                          <h4 className="text-xs font-bold text-white/90">{p.name}</h4>
                          <p className="text-[10px] text-white/50">{p.type}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <span className={`text-[10px] px-2 py-0.5 rounded uppercase font-bold border ${
                          p.status === "Colonized" ? "bg-green-500/20 text-green-400 border-green-500/30" : "bg-white/5 text-white/40 border-white/10"
                        }`}>
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
            <div className="bg-[#121520]/60 border border-cyan-500/40 p-5 rounded-xl space-y-5 shadow-2xl backdrop-blur-md">
              <div className="flex justify-between items-center border-b border-white/10 pb-3">
                <div>
                  <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-wider">🪐 EXOPLANET INSPECTOR</h3>
                  <p className="text-[10px] text-white/40">{selectedPlanet.name}</p>
                </div>
                <span className={`text-[10px] px-2 py-0.5 rounded uppercase font-mono font-bold border ${
                  selectedPlanet.status === "Colonized" ? "bg-green-500/20 text-green-300 border-green-500/30" : "bg-white/5 text-white/40 border-white/10"
                }`}>
                  {selectedPlanet.status}
                </span>
              </div>

              <div className="space-y-3 text-xs">
                <div className="bg-[#0d0f17] p-3 rounded border border-white/5 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-white/50">Planet Type:</span>
                    <span className="text-white/90 font-semibold">{selectedPlanet.type}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/50">Population:</span>
                    <span className="text-cyan-400 font-bold">{selectedPlanet.population.toLocaleString()} Units</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/50">Resource Yield:</span>
                    <span className="text-amber-400 font-bold">{selectedPlanet.output}</span>
                  </div>
                </div>

                {selectedPlanet.status === "Unexplored" ? (
                  <button
                    onClick={() => handleColonizePlanet(selectedPlanet)}
                    disabled={stats.dna < selectedPlanet.cost}
                    className="w-full min-h-[44px] py-3 bg-gradient-to-r from-purple-500/20 to-cyan-500/20 hover:from-purple-500/40 hover:to-cyan-500/40 border border-purple-400 text-purple-300 rounded-lg text-xs font-bold tracking-widest uppercase transition-all shadow-lg cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed flex flex-col items-center justify-center"
                  >
                    <span>🚀 DISPATCH COLONY SEEDER</span>
                    <span className="text-[9px] text-amber-400 font-mono">REQUIRES {selectedPlanet.cost} DNA</span>
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
      )}
    </div>
  );
};
