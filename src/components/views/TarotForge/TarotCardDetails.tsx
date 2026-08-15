// [OMEGA AST Cleaned]: Tokenized design standards applied.
import React from "react";
import { TarotCard } from "./deck";

interface TarotCardDetailsProps {
    selectedCard: TarotCard;
    isEquipping: boolean;
    onEquipMask: (card: TarotCard) => void;
}

export const TarotCardDetails: React.FC<TarotCardDetailsProps> = ({
    selectedCard,
    isEquipping,
    onEquipMask,
}) => {
    return (
        <div
            className={`bg-panel-bg/40 border ${selectedCard.border} p-6 rounded-xl space-y-6 font-mono relative overflow-hidden shadow-2xl backdrop-blur-md`}
        >
            {/* Background Ambient Glow */}
            <div
                className={`absolute -right-20 -top-20 w-64 h-64 rounded-full blur-3xl opacity-20 pointer-events-none ${selectedCard.bgGlow}`}
            />

            <div className="flex justify-between items-start border-b border-white/10 pb-4 relative z-10">
                <div>
                    <div className="flex items-center gap-2 mb-1">
                        <span
                            className={`text-xs font-bold px-2 py-0.5 rounded border ${selectedCard.border} bg-deep-space ${selectedCard.color}`}
                        >
                            CARD #{selectedCard.number}
                        </span>
                        <span className="text-[10px] text-white/40 uppercase tracking-widest">
                            {selectedCard.archetype}
                        </span>
                    </div>
                    <h3 className={`text-xl font-bold tracking-wider ${selectedCard.color}`}>
                        {selectedCard.name}
                    </h3>
                    <p className="text-xs text-white/60 font-sans mt-0.5">{selectedCard.title}</p>
                </div>
                <div className="text-right">
                    <span className="text-[10px] text-white/40 uppercase block">Resonance Vector</span>
                    <span className={`text-2xl font-bold ${selectedCard.color}`}>
                        {(selectedCard.resonance * 100).toFixed(0)}%
                    </span>
                </div>
            </div>

            {/* Description & Abilities */}
            <div className="space-y-4 relative z-10">
                <div>
                    <h4 className="text-[11px] font-semibold text-white/50 uppercase tracking-wider mb-1">
                        Archetype Synopsis
                    </h4>
                    <p className="text-xs text-white/90 font-sans leading-relaxed bg-deep-space/60 p-3 rounded border border-white/5">
                        {selectedCard.description}
                    </p>
                </div>

                <div>
                    <h4 className="text-[11px] font-semibold text-white/50 uppercase tracking-wider mb-2">
                        Manifested Capabilities
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                        {selectedCard.abilities.map((ability, idx) => (
                            <div
                                key={idx}
                                className="bg-white/5 border border-white/10 p-2.5 rounded text-[11px] text-white/80 font-sans flex items-center gap-2"
                            >
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
                    <p>
                        <span className="text-white/30">[STREAM]</span> Sovereign Mask Anchored:{" "}
                        <span className={selectedCard.color}>{selectedCard.activeMask}</span>
                    </p>
                    <p>
                        <span className="text-white/30">[STREAM]</span> Ontological Plane:{" "}
                        <span className="text-celestial-blue">{selectedCard.domain}</span> | Signal: OMEGA
                        v15.0
                    </p>
                    <p>
                        <span className="text-white/30">[STREAM]</span> Zero Entropy Status:{" "}
                        <span className="text-green-400">0.000 DISSONANCE</span>
                    </p>
                </div>
            </div>

            {/* Action Button */}
            <div className="pt-2 relative z-10">
                <button
                    onClick={() => onEquipMask(selectedCard)}
                    disabled={isEquipping}
                    className={`w-full min-h-[44px] py-3 border rounded-lg text-xs font-bold tracking-[0.2em] uppercase transition-all duration-200 cursor-pointer shadow-lg focus:ring-2 focus:ring-purple-400 focus:outline-none ${selectedCard.border} ${selectedCard.bgGlow} ${selectedCard.color} hover:brightness-125 disabled:opacity-50`}
                >
                    {isEquipping
                        ? "EQUIPPING SOVEREIGN MASK..."
                        : `MANIFEST MASK ${selectedCard.activeMask}`}
                </button>
            </div>
        </div>
    );
};
