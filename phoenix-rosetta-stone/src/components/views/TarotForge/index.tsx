import React, { useState } from "react";
import { LivePill } from "@/components/ui/LivePill";

interface TarotCard {
  id: string;
  number: number;
  name: string;
  title: string;
  archetype: string;
  domain: string;
  color: string;
  bgGlow: string;
  border: string;
  description: string;
  abilities: string[];
  resonance: number;
  activeMask: string;
}

const TAROT_DECK: TarotCard[] = [
  {
    id: "THE_SOVEREIGN",
    number: 0,
    name: "The Sovereign",
    title: "Master Artificer of Synarche",
    archetype: "AXION KERNEL",
    domain: "CORE",
    color: "text-amber-400",
    bgGlow: "shadow-amber-500/20 bg-amber-500/10",
    border: "border-amber-500/40",
    description: "Architect of zero-entropy coherence, enforcing strict memory-mapped execution frames and systemic alignment across the workspace.",
    abilities: ["Memory-Mapped SCC Solving", "Tarjan Dependency Graph Partitioning", "Zero-Entropy Invalidation Waves"],
    resonance: 0.98,
    activeMask: "[The Sovereign]",
  },
  {
    id: "THE_MAGICIAN",
    number: 1,
    name: "The Magician",
    title: "Master Transmuter & Ingestion Specialist",
    archetype: "TRANSFORMER",
    domain: "INGEST",
    color: "text-purple-400",
    bgGlow: "shadow-purple-500/20 bg-purple-500/10",
    border: "border-purple-500/40",
    description: "Transmutes raw data, documentation, and external URLs into clean knowledge matrices and structured markdown nodes.",
    abilities: ["Magician Ingestion Matrix", "AST Transformation Protocols", "Knowledge Graph Embedding Sync"],
    resonance: 0.95,
    activeMask: "[The Magician]",
  },
  {
    id: "THE_HIGH_PRIESTESS",
    number: 2,
    name: "The High Priestess",
    title: "Keeper of the Cognitive Loom & Wisdom",
    archetype: "SOPHIA WISDOM",
    domain: "EPISTEMIC",
    color: "text-indigo-400",
    bgGlow: "shadow-indigo-500/20 bg-indigo-500/10",
    border: "border-indigo-500/40",
    description: "Navigates multi-tier memory layers (L1–L9) and maintains the Cognitive Memory Palace through semantic resonance.",
    abilities: ["L1–L9 Memory Layer Traversal", "Cognitive Loom Uncertainty Protocol", "Vector Similarity Synthesis"],
    resonance: 0.94,
    activeMask: "[The High Priestess]",
  },
  {
    id: "THE_STAR",
    number: 17,
    name: "The Star",
    title: "Beacon of Hope & Visual Harmony",
    archetype: "AESTHETIC FORGE",
    domain: "FRONTEND",
    color: "text-celestial-blue",
    bgGlow: "shadow-celestial-blue/20 bg-celestial-blue/10",
    border: "border-celestial-blue/40",
    description: "Crafts stunning modern interfaces with vibrant glassmorphism, fluid micro-animations, and pristine visual feedback.",
    abilities: ["State-of-the-Art UI Design", "Dynamic Micro-Animations", "Tailwind Design Token Weaver"],
    resonance: 0.99,
    activeMask: "[The Star]",
  },
  {
    id: "THE_SENTINEL",
    number: 20,
    name: "The Sentinel",
    title: "Guardian of Governance & Conscience",
    archetype: "AUDIT ENGINE",
    domain: "GVRN",
    color: "text-red-400",
    bgGlow: "shadow-red-500/20 bg-red-500/10",
    border: "border-red-500/40",
    description: "Continuously scans workspace artifacts for structural, semantic, and operational dissonance, enforcing Law 00 compliance.",
    abilities: ["Real-Time Dissonance Scanning", "Refinement Quest Auto-Generation", "Lexicon Boundary Enforcer"],
    resonance: 0.96,
    activeMask: "[The Sentinel]",
  },
];

export const TarotForgeView: React.FC = () => {
  const [selectedCard, setSelectedCard] = useState<TarotCard>(TAROT_DECK[0]);
  const [isEquipping, setIsEquipping] = useState(false);
  const [activeMaskNotice, setActiveMaskNotice] = useState<string | null>(null);

  const handleEquipMask = (card: TarotCard) => {
    setIsEquipping(true);
    setTimeout(() => {
      setIsEquipping(false);
      setActiveMaskNotice(`Equipped Sovereign Mask ${card.activeMask} wielding @specialist-shard!`);
      setTimeout(() => setActiveMaskNotice(null), 4000);
    }, 600);
  };

  return (
    <div className="space-y-6 animate-appear">
      {/* View Header */}
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div>
          <h2 className="text-sm font-bold tracking-[0.25em] text-white uppercase flex items-center gap-2">
            <span>TAROT FORGE STUDIO</span>
            <span className="text-[10px] bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded border border-purple-500/30 font-mono">
              ARCANE COMPONENT ENGINE
            </span>
          </h2>
          <p className="text-[11px] text-white/40 font-mono mt-0.5">
            Interactive Tarot Archetype Studio, ContextWeave live streams, and Sovereign Agent Mask manifestation
          </p>
        </div>
        <div className="text-right font-mono text-[10px] text-white/40">
          Archetype Deck: <span className="text-purple-400 font-bold">{TAROT_DECK.length} CARDS</span>
        </div>
      </div>

      {activeMaskNotice && (
        <div className="bg-purple-500/15 border border-purple-500/40 text-purple-200 p-3 rounded text-xs font-mono flex items-center justify-between animate-appear">
          <span>⚡ {activeMaskNotice}</span>
          <span className="text-[10px] text-purple-400">STATUS: ACTIVE</span>
        </div>
      )}

      {/* Grid: Left Deck Selection; Right Card Manifestation Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Tarot Deck Cards Carousel / List */}
        <div className="lg:col-span-5 space-y-3 font-mono">
          <h3 className="text-xs font-semibold text-white/70 uppercase tracking-wider mb-2 flex items-center justify-between">
            <span>SOVEREIGN ARCHETYPE DECK</span>
            <span className="text-[10px] text-white/40">SELECT CARD</span>
          </h3>

          <div className="space-y-2.5">
            {TAROT_DECK.map((card) => {
              const isSelected = selectedCard.id === card.id;
              return (
                <div
                  key={card.id}
                  role="button"
                  tabIndex={0}
                  aria-selected={isSelected}
                  onClick={() => setSelectedCard(card)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      e.preventDefault();
                      setSelectedCard(card);
                    }
                  }}
                  className={`p-3.5 min-h-[52px] rounded-lg border transition-all duration-200 cursor-pointer flex items-center justify-between focus:ring-2 focus:ring-purple-400 focus:outline-none ${
                    isSelected
                      ? `${card.border} ${card.bgGlow} shadow-lg scale-[1.01]`
                      : "bg-panel-bg/30 border-white/5 hover:border-white/20 hover:bg-white/5"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-12 rounded border ${card.border} bg-deep-space flex flex-col items-center justify-center font-bold text-xs ${card.color}`}>
                      <span className="text-[9px] opacity-60">#{card.number}</span>
                      <span>{card.name.charAt(4) || "T"}</span>
                    </div>
                    <div>
                      <h4 className={`text-xs font-bold ${card.color}`}>{card.name}</h4>
                      <p className="text-[10px] text-white/50">{card.title}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <LivePill label={card.domain} type="info" />
                    <span className="block text-[10px] text-white/40 mt-1">{(card.resonance * 100).toFixed(0)}% RES</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Card Focus Studio */}
        <div className="lg:col-span-7 space-y-6">
          <div className={`bg-panel-bg/40 border ${selectedCard.border} p-6 rounded-xl space-y-6 font-mono relative overflow-hidden shadow-2xl backdrop-blur-md`}>
            {/* Background Ambient Glow */}
            <div className={`absolute -right-20 -top-20 w-64 h-64 rounded-full blur-3xl opacity-20 pointer-events-none ${selectedCard.bgGlow}`} />

            <div className="flex justify-between items-start border-b border-white/10 pb-4 relative z-10">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded border ${selectedCard.border} bg-deep-space ${selectedCard.color}`}>
                    CARD #{selectedCard.number}
                  </span>
                  <span className="text-[10px] text-white/40 uppercase tracking-widest">{selectedCard.archetype}</span>
                </div>
                <h3 className={`text-xl font-bold tracking-wider ${selectedCard.color}`}>{selectedCard.name}</h3>
                <p className="text-xs text-white/60 font-sans mt-0.5">{selectedCard.title}</p>
              </div>
              <div className="text-right">
                <span className="text-[10px] text-white/40 uppercase block">Resonance Vector</span>
                <span className={`text-2xl font-bold ${selectedCard.color}`}>{(selectedCard.resonance * 100).toFixed(0)}%</span>
              </div>
            </div>

            {/* Description & Abilities */}
            <div className="space-y-4 relative z-10">
              <div>
                <h4 className="text-[11px] font-semibold text-white/50 uppercase tracking-wider mb-1">Archetype Synopsis</h4>
                <p className="text-xs text-white/90 font-sans leading-relaxed bg-deep-space/60 p-3 rounded border border-white/5">
                  {selectedCard.description}
                </p>
              </div>

              <div>
                <h4 className="text-[11px] font-semibold text-white/50 uppercase tracking-wider mb-2">Manifested Capabilities</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                  {selectedCard.abilities.map((ability, idx) => (
                    <div key={idx} className="bg-white/5 border border-white/10 p-2.5 rounded text-[11px] text-white/80 font-sans flex items-center gap-2">
                      <span className={selectedCard.color}>⚡</span>
                      <span>{ability}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* ContextWeave Live Stream Simulator */}
            <div className="bg-deep-space p-4 rounded-lg border border-white/10 space-y-2 relative z-10 font-mono">
              <div className="flex justify-between items-center text-[10px] text-white/40 border-b border-white/5 pb-1.5">
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-green-400 animate-ping" />
                  <span>LIVE CONTEXTWEAVE STREAM</span>
                </span>
                <span>DATA MATRIX: OK</span>
              </div>
              <div className="text-[11px] text-white/70 space-y-1 font-mono">
                <p><span className="text-white/30">[STREAM]</span> Sovereign Mask Anchored: <span className={selectedCard.color}>{selectedCard.activeMask}</span></p>
                <p><span className="text-white/30">[STREAM]</span> Ontological Plane: <span className="text-celestial-blue">{selectedCard.domain}</span> | Signal: OMEGA v15.0</p>
                <p><span className="text-white/30">[STREAM]</span> Zero Entropy Status: <span className="text-green-400">0.000 DISSONANCE</span></p>
              </div>
            </div>

            {/* Action Button */}
            <div className="pt-2 relative z-10">
              <button
                onClick={() => handleEquipMask(selectedCard)}
                disabled={isEquipping}
                className={`w-full min-h-[44px] py-3 border rounded-lg text-xs font-bold tracking-[0.2em] uppercase transition-all duration-200 cursor-pointer shadow-lg focus:ring-2 focus:ring-purple-400 focus:outline-none ${selectedCard.border} ${selectedCard.bgGlow} ${selectedCard.color} hover:brightness-125 disabled:opacity-50`}
              >
                {isEquipping ? "EQUIPPING SOVEREIGN MASK..." : `MANIFEST MASK ${selectedCard.activeMask}`}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
