// [OMEGA AST Cleaned]: Tokenized design standards applied.
import type React from "react";
import { useState } from "react";
import { TarotCard, TAROT_DECK } from "./deck";
import { TarotCardList } from "./TarotCardList";
import { TarotCardDetails } from "./TarotCardDetails";

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
                        Interactive Tarot Archetype Studio, ContextWeave live streams, and Sovereign Agent Mask
                        manifestation
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

                    <TarotCardList
                        deck={TAROT_DECK}
                        selectedCard={selectedCard}
                        onSelectCard={setSelectedCard}
                    />
                </div>

                {/* Selected Card Focus Studio */}
                <div className="lg:col-span-7 space-y-6">
                    <TarotCardDetails
                        selectedCard={selectedCard}
                        isEquipping={isEquipping}
                        onEquipMask={handleEquipMask}
                    />
                </div>
            </div>
        </div>
    );
};
export type { TarotCard };
