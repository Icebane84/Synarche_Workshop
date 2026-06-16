/**
 * artifact_anchor:
 * - id: UMB-UI-DISSONANCE-STREAM
 * - type: COMPONENT
 */
import { useState } from "react";

export enum DissonanceType {
    ConceptualInconsistency = "CONCEPTUAL_INCONSISTENCY",
    LogicalContradiction = "LOGICAL_CONTRADICTION",
    ThematicMismatch = "THEMATIC_MISMATCH",
    EthicalViolation = "ETHICAL_VIOLATION",
    ContextualRegression = "CONTEXTUAL_REGRESSION",
    StalledIntent = "STALLED_INTENT",
}

export interface CoherenceDissonance {
    id: string;
    type: DissonanceType;
    description: string;
    confidence: number; // 0.0 to 1.0
    sourceLogs: string[];
    impactPrediction: string;
    status: "DETECTED" | "ANALYZED" | "RESOLVED" | "UNRESOLVABLE";
}

interface DissonanceStreamProps {
    dissonances: CoherenceDissonance[];
    onResolveClick?: (id: string) => void;
}

export default function DissonanceStream({ dissonances, onResolveClick }: DissonanceStreamProps) {
    const [expandedId, setExpandedId] = useState<string | null>(null);

    return (
        <div className="flex flex-col gap-4 w-full max-w-2xl bg-[#00001a] p-5 rounded-xl shadow-2xl border border-gray-800 overflow-y-auto max-h-[600px] scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-transparent">
            <h2 className="text-xl font-semibold text-[#77B5FE] drop-shadow-[0_0_8px_rgba(119,181,254,0.8)] sticky top-0 bg-[#00001a] z-10 py-2 border-b border-gray-800">
                Dissonance Stream
            </h2>

            {dissonances.length === 0 ? (
                <div className="text-gray-500 italic text-center py-8">
                    No active dissonances detected. System is coherent.
                </div>
            ) : (
                dissonances.map((dissonance) => {
                    const isExpanded = expandedId === dissonance.id;
                    return (
                        <div
                            key={dissonance.id}
                            className={`relative p-4 rounded-lg border transition-all duration-300 cursor-pointer ${
                                dissonance.status === "RESOLVED"
                                    ? "border-green-800/50 bg-green-900/10"
                                    : "border-red-900/50 bg-red-900/20 hover:border-red-500/80 hover:shadow-[0_0_15px_rgba(220,38,38,0.3)]"
                            }`}
                            onClick={() => setExpandedId(isExpanded ? null : dissonance.id)}
                        >
                            <div className="flex justify-between items-start mb-2">
                                <span className="text-sm font-mono text-red-400 font-bold uppercase tracking-wider">
                                    {dissonance.type.replace("_", " ")}
                                </span>
                                <span className="text-xs font-mono px-2 py-1 rounded bg-black/40 text-gray-300 border border-gray-700">
                                    {dissonance.status}
                                </span>
                            </div>
                            <p className="text-gray-200 text-sm">{dissonance.description}</p>

                            {isExpanded && (
                                <div className="mt-4 pt-4 border-t border-red-900/50 flex flex-col gap-3 animate-in fade-in duration-200">
                                    <div>
                                        <span className="text-xs text-gray-500 uppercase">Impact Prediction:</span>
                                        <p className="text-sm text-red-300/80">{dissonance.impactPrediction}</p>
                                    </div>
                                    <div className="flex justify-between items-end mt-2">
                                        <div className="flex flex-col gap-1">
                                            <span className="text-xs text-gray-500 uppercase">Confidence Level:</span>
                                            <span className="text-sm text-[#77B5FE] font-mono">
                                                {(dissonance.confidence * 100).toFixed(1)}%
                                            </span>
                                        </div>
                                        {onResolveClick && dissonance.status !== "RESOLVED" && (
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    onResolveClick(dissonance.id);
                                                }}
                                                className="px-4 py-2 text-xs font-bold text-white bg-red-800/60 hover:bg-red-700 rounded transition-colors shadow-[0_0_10px_rgba(153,27,27,0.5)] hover:shadow-[0_0_15px_rgba(220,38,38,0.8)]"
                                            >
                                                INITIATE SYNTHESIS
                                            </button>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    );
                })
            )}
        </div>
    );
}
