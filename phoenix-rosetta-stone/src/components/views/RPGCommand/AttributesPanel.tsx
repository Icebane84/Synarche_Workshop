import React from "react";
import { StatBar } from "@/components/ui/StatBar";

interface AttributesPanelProps {
  stats: any;
  isLoading: boolean;
}

export const AttributesPanel: React.FC<AttributesPanelProps> = ({ stats, isLoading }) => {
  if (isLoading) {
    return (
      <div className="py-8 text-center text-xs text-white/30 animate-pulse font-mono">
        Calculating stat modifiers...
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="py-8 text-center text-xs text-white/30 italic font-mono">
        No attributes found for current entity.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="space-y-4">
        <StatBar label="Coherence Index" value={stats.coherence_index ?? 0} colorClass="bg-coherence-indigo" />
        <StatBar label="Synergy Rate" value={stats.synergy ?? 0} colorClass="bg-synergy-emerald" />
        <StatBar label="Adaptability Matrix" value={stats.adaptability ?? 0} colorClass="bg-adapt-amber" />
        <StatBar label="Transparency Coefficient" value={stats.transparency ?? 0} colorClass="bg-transparency-silver" />
      </div>
      <div className="space-y-4">
        <StatBar label="Ascension Level" value={stats.form_ascension_state ?? 0} colorClass="bg-form-ascension" />
        <StatBar label="Semantic Friction" value={stats.semantic_friction_resonance ?? 0} colorClass="bg-semantic-friction" />
        <StatBar label="Creative Spark" value={stats.creative_spark ?? 0} colorClass="bg-creative-spark" />
      </div>
    </div>
  );
};
