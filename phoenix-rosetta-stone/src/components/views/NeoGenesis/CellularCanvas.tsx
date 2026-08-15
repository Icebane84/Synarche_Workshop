import React, { useEffect, useRef } from "react";
import { OrganismStats, Nutrient, PredatorICE, ToxicZone, Particle } from "./NeoGenesisConstants";

interface CellularCanvasProps {
  stats: OrganismStats;
  setStats: React.Dispatch<React.SetStateAction<OrganismStats>>;
  audioEnabled: boolean;
  playSound: (type: "absorb" | "mutagen" | "hit" | "ascend" | "build") => void;
  setLogs: React.Dispatch<React.SetStateAction<string[]>>;
}

const getRandomFloat = (): number => {
  const array = new Uint32Array(1);
  crypto.getRandomValues(array);
  return array[0] / (0xffffffff + 1);
};

export const CellularCanvas: React.FC<CellularCanvasProps> = ({
  stats,
  setStats,
  audioEnabled,
  playSound,
  setLogs,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const playerRef = useRef({ x: 300, y: 200, radius: 14, color: "#00f0ff" });
  const nutrientsRef = useRef<Nutrient[]>([]);
  const predatorsRef = useRef<PredatorICE[]>([]);
  const toxicZonesRef = useRef<ToxicZone[]>([]);
  const particlesRef = useRef<Particle[]>([]);
  const shakeRef = useRef<number>(0);
  const keysRef = useRef<{ [key: string]: boolean }>({});
  const lastDamageTimeRef = useRef<number>(0);

  // Particle Spawner
  const spawnParticleSparks = (x: number, y: number, color: string, count = 12) => {
    for (let i = 0; i < count; i++) {
      const angle = getRandomFloat() * Math.PI * 2;
      const speed = getRandomFloat() * 4 + 1;
      particlesRef.current.push({
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        color,
        life: 0,
        maxLife: getRandomFloat() * 20 + 15,
        size: getRandomFloat() * 3 + 2,
      });
    }
  };

  // Spawn initial nutrients/predators
  useEffect(() => {
    const nutArr: Nutrient[] = [];
    for (let i = 0; i < 25; i++) {
      nutArr.push({
        x: getRandomFloat() * 600,
        y: getRandomFloat() * 400,
        size: getRandomFloat() * 4 + 3,
        color: getRandomFloat() > 0.3 ? "#00f0ff" : getRandomFloat() > 0.5 ? "#a855f7" : "#f59e0b",
        type: getRandomFloat() > 0.3 ? "amino" : getRandomFloat() > 0.5 ? "lipid" : "mutagen",
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

  // Keyboard controls
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

  // Main game loop
  useEffect(() => {
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
        const dx = (getRandomFloat() - 0.5) * shakeRef.current;
        const dy = (getRandomFloat() - 0.5) * shakeRef.current;
        ctx.translate(dx, dy);
        shakeRef.current *= 0.85;
        if (shakeRef.current < 0.5) shakeRef.current = 0;
      }

      // Draw background
      ctx.fillStyle = "#090a0f";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Grid
      ctx.strokeStyle = "rgba(0, 240, 255, 0.05)";
      ctx.lineWidth = 1;
      for (let x = 0; x < canvas.width; x += 30) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke(); }
      for (let y = 0; y < canvas.height; y += 30) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke(); }

      // Toxic zones
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

      // Nutrients
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

          n.x = getRandomFloat() * canvas.width;
          n.y = getRandomFloat() * canvas.height;
          const dnaGained = n.type === "mutagen" ? 6 : 3;
          setStats((prev) => {
            const newDna = prev.dna + dnaGained * prev.ingestion;
            const newReadiness = Math.min(100, prev.readiness + 2);
            const newHp = Math.min(prev.maxHp, prev.hp + 1);
            return { ...prev, dna: newDna, readiness: newReadiness, hp: newHp };
          });
        }
      });

      // Predators
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

      // Particles
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

      // Player circle
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
  }, [stats.speed, stats.ingestion, stats.armor, audioEnabled]);

  return (
    <div className="relative border border-white/10 rounded-lg overflow-hidden bg-black/60 shadow-inner">
      <canvas ref={canvasRef} width={600} height={400} className="w-full h-auto" />
      <div className="absolute bottom-3 left-3 text-[10px] text-white/50 bg-black/70 px-2 py-1 rounded border border-white/5">
        Move: W, A, S, D or Arrows
      </div>
    </div>
  );
};
