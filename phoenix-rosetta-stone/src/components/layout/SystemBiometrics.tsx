import React from "react";
import { useSystemMetrics } from "@core/hooks/useSystemMetrics";

const Sparkline: React.FC<{ data: number[]; color: string; min?: number; max?: number }> = ({
  data,
  color,
  min = 0,
  max = 100,
}) => {
  const width = 44;
  const height = 12;

  const points = data
    .map((val, i) => {
      const x = (i / (data.length - 1)) * width;
      const clampedVal = Math.max(min, Math.min(max, val));
      const normalizedY = (clampedVal - min) / (max - min);
      const y = height - normalizedY * height;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  return (
    <svg width={width} height={height} className="overflow-visible opacity-60 group-hover:opacity-100 transition-opacity duration-300">
      <polyline
        points={points}
        fill="none"
        stroke={color}
        strokeWidth="1.2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
};

export const SystemBiometrics: React.FC = () => {
  const metrics = useSystemMetrics();

  const currentFps = metrics.pulse[metrics.pulse.length - 1] || 60;
  const currentLoad = ((metrics.pressure[metrics.pressure.length - 1] || 0.15) * 100).toFixed(0);
  const currentTemp = ((metrics.temp[metrics.temp.length - 1] || 0) * 100).toFixed(0);

  return (
    <div className="w-full flex flex-col items-center gap-3 pt-4 border-t border-white/5 bg-black/10">
      {/* Pulse (FPS) */}
      <div className="group flex flex-col items-center justify-center gap-0.5 cursor-help" title="System Pulse (Refresh Rate)">
        <div className="flex items-center gap-1">
          {/* Activity / Pulse Icon */}
          <svg className="w-3 h-3 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
          </svg>
          <span className="text-[9px] font-mono text-emerald-300 font-bold">{currentFps}Hz</span>
        </div>
        <Sparkline data={metrics.pulse} color="#34d399" min={0} max={60} />
      </div>

      {/* Pressure (Simulated Load) */}
      <div className="group flex flex-col items-center justify-center gap-0.5 cursor-help" title="Cognitive Pressure (System Load)">
        <div className="flex items-center gap-1">
          {/* Gauge Icon */}
          <svg className="w-3 h-3 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <path d="M12 2a10 10 0 0 1 10 10c0 2.21-.89 4.21-2.34 5.66L18 16a8 8 0 0 0-12 0l-1.66 1.66A9.92 9.92 0 0 1 2 12c0-5.52 4.48-10 10-10z" />
            <polyline points="12 12 16 8" />
          </svg>
          <span className="text-[9px] font-mono text-amber-300 font-bold">{currentLoad}%</span>
        </div>
        <Sparkline data={metrics.pressure.map((v) => v * 100)} color="#fbbf24" min={0} max={100} />
      </div>

      {/* Temperature (Entropy) */}
      <div className="group flex flex-col items-center justify-center gap-0.5 cursor-help" title="Entropy Index (Cognitive Strain)">
        <div className="flex items-center gap-1">
          {/* Thermometer Icon */}
          <svg className="w-3 h-3 text-rose-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z" />
          </svg>
          <span className="text-[9px] font-mono text-rose-300 font-bold">{currentTemp}°</span>
        </div>
        <Sparkline data={metrics.temp.map((v) => v * 100)} color="#fb7185" min={0} max={100} />
      </div>
    </div>
  );
};
