import React from "react";

interface LivePillProps {
  label: string;
  type?: "active" | "fading" | "consolidated" | "archived" | "error" | "warning" | "info";
  className?: string;
}

export const LivePill: React.FC<LivePillProps> = ({ label, type = "info", className = "" }) => {
  const styles = {
    active: "bg-status-active/10 border-status-active/30 text-status-active",
    fading: "bg-status-fading/10 border-status-fading/30 text-status-fading",
    consolidated: "bg-status-consolidated/10 border-status-consolidated/30 text-status-consolidated",
    archived: "bg-status-archived/10 border-status-archived/30 text-status-archived",
    error: "bg-status-error/10 border-status-error/30 text-status-error",
    warning: "bg-status-warning/10 border-status-warning/30 text-status-warning",
    info: "bg-celestial-blue/10 border-celestial-blue/30 text-celestial-blue",
  };

  const dots = {
    active: "bg-status-active shadow-[0_0_8px_#10b981]",
    fading: "bg-status-fading shadow-[0_0_8px_#f59e0b]",
    consolidated: "bg-status-consolidated shadow-[0_0_8px_#6366f1]",
    archived: "bg-status-archived shadow-none",
    error: "bg-status-error shadow-[0_0_8px_#ef4444]",
    warning: "bg-status-warning shadow-[0_0_8px_#f97316]",
    info: "bg-celestial-blue shadow-[0_0_8px_#77b5fe]",
  };

  return (
    <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 border rounded font-mono text-[10px] uppercase tracking-wider select-none ${styles[type]} ${className}`}>
      <span className={`w-1.5 h-1.5 rounded-full animate-pulse-glow ${dots[type]}`} />
      {label}
    </span>
  );
};
