import React from "react";

interface StatBarProps {
  label: string;
  value: number;
  max?: number;
  colorClass?: string; // e.g. bg-coherence-indigo, bg-synergy-emerald, etc.
  showDetails?: boolean;
}

export const StatBar: React.FC<StatBarProps> = ({
  label,
  value,
  max = 100,
  colorClass = "bg-celestial-blue",
  showDetails = true,
}) => {
  const percentage = Math.max(0, Math.min(100, (value / max) * 100));

  return (
    <div className="font-mono space-y-1">
      <div className="flex justify-between text-xs tracking-wider">
        <span className="text-white/60 uppercase">{label}</span>
        {showDetails && (
          <span className="text-white/80 font-semibold text-data">
            {value.toLocaleString()} / {max.toLocaleString()} ({Math.round(percentage)}%)
          </span>
        )}
      </div>
      <div className="h-2 w-full bg-white/5 border border-white/10 rounded-sm overflow-hidden p-[1px]">
        <div
          className={`h-full rounded-sm transition-all duration-500 ease-out ${colorClass}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
