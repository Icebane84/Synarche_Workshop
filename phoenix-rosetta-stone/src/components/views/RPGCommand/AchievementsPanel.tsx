import React from "react";

interface AchievementsPanelProps {
  achievements: any[];
}

export const AchievementsPanel: React.FC<AchievementsPanelProps> = ({ achievements }) => {
  if (achievements.length === 0) {
    return (
      <div className="bg-panel-bg/25 border border-white/5 p-6 rounded-lg text-center text-xs text-white/30 italic font-mono">
        No achievements unlocked yet.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {achievements.map((ach, idx) => (
        <div
          key={ach.id || ach.title || `ach-${idx}`}
          className="bg-panel-bg/40 border border-white/5 rounded-lg p-3 font-mono text-xs flex gap-3 relative overflow-hidden"
        >
          <div className="text-xl">🏆</div>
          <div>
            <h4 className="font-bold text-white/95">{ach.title || "First Steps"}</h4>
            <p className="text-[10px] text-white/50">{ach.description || "Initialize the Phoenix core."}</p>
            <div className="text-[9px] text-chris-amber font-semibold mt-1">+1,000 XP • +100 Stardust</div>
          </div>
        </div>
      ))}
    </div>
  );
};
