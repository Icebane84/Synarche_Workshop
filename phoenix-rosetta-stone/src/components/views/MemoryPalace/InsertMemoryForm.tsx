import React, { useState } from "react";

interface InsertMemoryFormProps {
    onInsert: (memory: { content: string; domain: string; memory_layer: number }) => Promise<void>;
}

export const InsertMemoryForm: React.FC<InsertMemoryFormProps> = ({ onInsert }) => {
    const [newContent, setNewContent] = useState("");
    const [newDomain, setNewDomain] = useState("Axiom");
    const [newLayer, setNewLayer] = useState(1);
    const [isInserting, setIsInserting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newContent.trim()) return;

        setIsInserting(true);
        try {
            await onInsert({
                content: newContent,
                domain: newDomain,
                memory_layer: newLayer,
            });
            setNewContent("");
        } catch (err) {
            console.error(err);
        } finally {
            setIsInserting(false);
        }
    };

    return (
        <div className="bg-panel-bg/40 border border-white/5 p-4 rounded-lg space-y-4 font-mono">
            <h3 className="text-xs font-semibold text-white/70 uppercase tracking-wider">
                ENGRAVE MEMORY CHIP
            </h3>
            <form onSubmit={handleSubmit} className="space-y-3">
                <div>
                    <label className="block text-[10px] text-chrome mb-1">Domain</label>
                    <select
                        value={newDomain}
                        onChange={(e) => setNewDomain(e.target.value)}
                        className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none"
                    >
                        <option value="Axiom">Axiom</option>
                        <option value="Epistemic">Epistemic</option>
                        <option value="RPG">RPG</option>
                        <option value="Substrate">Substrate</option>
                    </select>
                </div>

                <div>
                    <label className="block text-[10px] text-chrome mb-1">Layer Depth</label>
                    <input
                        type="number"
                        min={1}
                        max={9}
                        value={newLayer}
                        onChange={(e) => setNewLayer(Number(e.target.value))}
                        className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none font-mono"
                    />
                </div>

                <div>
                    <label className="block text-[10px] text-chrome mb-1">Content</label>
                    <textarea
                        value={newContent}
                        onChange={(e) => setNewContent(e.target.value)}
                        placeholder="Log memory context details..."
                        rows={4}
                        className="w-full bg-deep-space border border-white/10 rounded px-2.5 py-1.5 text-xs text-white/80 focus:border-celestial-blue/50 focus:outline-none font-sans"
                    />
                </div>

                <button
                    type="submit"
                    disabled={isInserting || !newContent.trim()}
                    className="w-full py-2 bg-celestial-blue/15 hover:bg-celestial-blue/25 border border-celestial-blue/40 hover:border-celestial-blue/60 text-celestial-blue rounded text-xs tracking-widest font-semibold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                >
                    {isInserting ? "ENGRAVING..." : "ENGRAVE CHIP"}
                </button>
            </form>
        </div>
    );
};
