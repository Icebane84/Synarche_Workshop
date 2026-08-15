import React from "react";
import { LivePill } from "@components/ui/LivePill";
import { TarotCard } from "./deck";

interface TarotCardListProps {
    deck: TarotCard[];
    selectedCard: TarotCard;
    onSelectCard: (card: TarotCard) => void;
}

export const TarotCardList: React.FC<TarotCardListProps> = ({
    deck,
    selectedCard,
    onSelectCard,
}) => {
    return (
        <div className="space-y-2.5">
            {deck.map((card, idx) => {
                const isSelected = selectedCard.id === card.id;
                return (
                    <div
                        key={card.id || card.name || `card-${idx}`}
                        role="button"
                        tabIndex={0}
                        aria-selected={isSelected}
                        onClick={() => onSelectCard(card)}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === " ") {
                                e.preventDefault();
                                onSelectCard(card);
                            }
                        }}
                        className={`p-3.5 min-h-[52px] rounded-lg border transition-all duration-200 cursor-pointer flex items-center justify-between focus:ring-2 focus:ring-purple-400 focus:outline-none ${
                            isSelected
                                ? `${card.border} ${card.bgGlow} shadow-lg scale-[1.01]`
                                : "bg-panel-bg/30 border-white/5 hover:border-white/20 hover:bg-white/5"
                        }`}
                    >
                        <div className="flex items-center gap-3">
                            <div
                                className={`w-10 h-12 rounded border ${card.border} bg-deep-space flex flex-col items-center justify-center font-bold text-xs ${card.color}`}
                            >
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
                            <span className="block text-[10px] text-white/40 mt-1">
                                {(card.resonance * 100).toFixed(0)}% RES
                            </span>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};
