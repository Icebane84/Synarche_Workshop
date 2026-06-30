import { AnimatePresence, motion } from "framer-motion";
import { Clock, Database, Maximize2, Minimize2, Search, Tag, X, Zap } from "lucide-react";
import React, { useEffect, useMemo, useRef, useState } from "react";
import ForceGraph3D from "react-force-graph-3d";
import { useSensoryResonance } from "../../hooks/useSensoryResonance";
import { MemoryNode, useMemoryStore } from "../../store/memoryStore";

/**
 * Memory Palace [OMEGA v15.0]
 * 3D Kinetic Force Graph Visualization of the Cognitive Substrate.
 */

interface GraphNode extends MemoryNode {
    val: number;
    color: string;
    x?: number;
    y?: number;
    z?: number;
    opacity?: number;
}

interface ForceGraphMethods {
    cameraPosition: (
        position: { x?: number; y?: number; z?: number },
        lookAt?: GraphNode | object | null,
        transitionMs?: number,
    ) => void;
}

const MemoryPalacePage: React.FC = () => {
    const nodes = useMemoryStore((state) => state.nodes);
    const links = useMemoryStore((state) => state.links);
    const fetchMemories = useMemoryStore((state) => state.fetchMemories);
    const resonance = useSensoryResonance();
    const graphRef = useRef<any>(undefined);

    const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [isFullscreen, setIsFullscreen] = useState(false);

    useEffect(() => {
        void fetchMemories();
    }, [fetchMemories]);

    // Graph Settings
    const graphData = useMemo(
        () => ({
            nodes: nodes.map((n) => {
                let nodeColor = "#94A3B8"; // default Kinetic
                if (n.domain === "Codebase") {
                    if (n.tags.includes("dir:components") || n.tags.includes("dir:ui")) {
                        nodeColor = "#06B6D4"; // Cyan for components
                    } else if (n.tags.includes("dir:store") || n.tags.includes("dir:state")) {
                        nodeColor = "#10B981"; // Emerald for state/stores
                    } else if (
                        n.tags.includes("dir:services") ||
                        n.tags.includes("dir:core") ||
                        n.tags.includes("dir:hooks")
                    ) {
                        nodeColor = "#6366F1"; // Indigo for core/services
                    } else {
                        nodeColor = "#F59E0B"; // Amber for utilities/types
                    }
                } else {
                    nodeColor =
                        n.layer === 1
                            ? "#FCD34D" // Gem
                            : n.layer === 4
                              ? "#818CF8" // Sovereign
                              : n.layer === 3
                                ? "#2DD4BF" // Semantic
                                : "#94A3B8";
                }
                return {
                    ...n,
                    val: n.activation * 10 + 4, // Make them a bit larger and prominent
                    color: nodeColor,
                };
            }),
            links: links,
        }),
        [nodes, links],
    );

    const handleNodeClick = (node: object) => {
        const gNode = node as GraphNode;
        setSelectedNode(gNode);
        if (graphRef.current && gNode.x !== undefined && gNode.y !== undefined && gNode.z !== undefined) {
            // Aim at node from outside it
            const distance = 40;
            const distRatio = 1 + distance / Math.hypot(gNode.x, gNode.y, gNode.z);

            graphRef.current.cameraPosition(
                { x: gNode.x * distRatio, y: gNode.y * distRatio, z: gNode.z * distRatio }, // new pos
                gNode, // lookAt property
                3000, // transition duration
            );
        }
    };

    const filteredData = useMemo(() => {
        if (!searchQuery) return graphData;
        const lower = searchQuery.toLowerCase();
        return {
            nodes: graphData.nodes.map((n) => ({
                ...n,
                opacity: n.content.toLowerCase().includes(lower) || n.domain.toLowerCase().includes(lower) ? 1 : 0.1,
            })),
            links: graphData.links,
        };
    }, [graphData, searchQuery]);

    return (
        <div
            className={`relative h-full w-full bg-black overflow-hidden flex flex-col transition-all duration-700 contain-content ${isFullscreen ? "fixed inset-0 z-[100]" : ""}`}
        >
            {/* Header / UI Overlay */}
            <div className="absolute top-6 left-6 z-10 flex flex-col gap-2 pointer-events-none">
                <motion.h2
                    className="text-3xl font-thin tracking-[0.3em] text-white uppercase"
                    style={{ textShadow: `0 0 ${resonance.blur} ${resonance.accentColor}` }}
                >
                    Memory Palace
                </motion.h2>
                <div className="flex items-center gap-4">
                    <p className="text-[10px] font-mono text-cyan-500/60 tracking-widest uppercase">
                        Kinetic Force Projection [Axion v1.0]
                    </p>
                    <div className="flex items-center gap-1">
                        <div className="w-1 h-1 bg-emerald-500 rounded-full animate-pulse" />
                        <span className="text-[8px] text-emerald-500/80 font-bold uppercase tracking-tighter">
                            Live Sync
                        </span>
                    </div>
                </div>
            </div>

            {/* Controls */}
            <div className="absolute top-6 right-6 z-10 flex items-center gap-3">
                <div className="glass-panel px-3 py-1.5 flex items-center gap-2 bg-black/40 backdrop-blur-md border-white/5">
                    <Search size={14} className="text-gray-500" />
                    <input
                        type="text"
                        placeholder="SEARCH MEMORY..."
                        value={searchQuery}
                        onChange={(e) => {
                            setSearchQuery(e.target.value);
                        }}
                        className="bg-transparent text-[10px] font-mono text-white focus:outline-none w-32 border-none"
                    />
                </div>
                <button
                    onClick={() => {
                        setIsFullscreen(!isFullscreen);
                    }}
                    className="p-2 glass-panel hover:bg-white/5 text-gray-400 hover:text-white transition-all"
                >
                    {isFullscreen ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
                </button>
            </div>

            {/* Main Graph View */}
            <div className="flex-1 cursor-crosshair">
                <ForceGraph3D
                    ref={graphRef}
                    graphData={filteredData}
                    nodeLabel={(node: object) =>
                        `<div class="p-2 bg-black/80 border border-white/10 text-xs font-mono">${(node as GraphNode).content.slice(0, 50)}...</div>`
                    }
                    nodeColor="color"
                    nodeVal="val"
                    linkWidth={1}
                    linkColor={() => "rgba(255, 255, 255, 0.05)"}
                    backgroundColor="#000000"
                    onNodeClick={handleNodeClick}
                    nodeOpacity={0.9}
                    enableNodeDrag={false}
                />
            </div>

            {/* Node Detail Side Panel */}
            <AnimatePresence>
                {selectedNode && (
                    <motion.div
                        initial={{ x: 400 }}
                        animate={{ x: 0 }}
                        exit={{ x: 400 }}
                        className="absolute top-0 right-0 bottom-0 w-80 glass-panel border-l border-white/10 bg-black/60 backdrop-blur-3xl z-20 p-8 flex flex-col gap-6 overflow-y-auto"
                    >
                        <div className="flex justify-between items-start">
                            <div className="flex items-center gap-2">
                                <Database size={16} className="text-cyan-400" />
                                <span className="text-[10px] font-mono text-gray-500 uppercase tracking-widest">
                                    Fragment ID: {selectedNode.id}
                                </span>
                            </div>
                            <button
                                onClick={() => {
                                    setSelectedNode(null);
                                }}
                                className="text-gray-500 hover:text-white"
                            >
                                <X size={20} />
                            </button>
                        </div>

                        <div className="space-y-2">
                            <h3 className="text-xs font-bold text-gray-400 uppercase tracking-tighter">Content</h3>
                            <p className="text-sm font-light leading-relaxed text-gray-200 bg-white/5 p-4 rounded-lg border border-white/5">
                                {selectedNode.content}
                            </p>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="p-3 bg-white/5 rounded-lg border border-white/5">
                                <div className="flex items-center gap-2 text-cyan-400 mb-1">
                                    <Zap size={12} />
                                    <span className="text-[9px] font-bold uppercase tracking-widest">Activation</span>
                                </div>
                                <div className="text-lg font-thin text-white">
                                    {(selectedNode.activation * 100).toFixed(0)}%
                                </div>
                            </div>
                            <div className="p-3 bg-white/5 rounded-lg border border-white/5">
                                <div className="flex items-center gap-2 text-indigo-400 mb-1">
                                    <Clock size={12} />
                                    <span className="text-[9px] font-bold uppercase tracking-widest">Layer</span>
                                </div>
                                <div className="text-lg font-thin text-white">L{selectedNode.layer}</div>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <h3 className="text-xs font-bold text-gray-400 uppercase tracking-tighter">
                                Domain & Context
                            </h3>
                            <div className="px-3 py-1.5 bg-cyan-500/10 border border-cyan-500/20 rounded text-[10px] font-mono text-cyan-300 inline-block uppercase">
                                {selectedNode.domain}
                            </div>
                        </div>

                        {selectedNode.tags.length > 0 && (
                            <div className="space-y-3">
                                <h3 className="text-xs font-bold text-gray-400 uppercase tracking-tighter">
                                    Neural Indices (Tags)
                                </h3>
                                <div className="flex flex-wrap gap-2">
                                    {selectedNode.tags.map((tag: string) => (
                                        <div
                                            key={tag}
                                            className="flex items-center gap-1 px-2 py-1 bg-white/5 border border-white/10 rounded-full text-[9px] text-gray-400"
                                        >
                                            <Tag size={8} />
                                            {tag}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        <div className="mt-auto pt-6 border-t border-white/5">
                            <p className="text-[8px] font-mono text-gray-600 uppercase tracking-widest">
                                Crystallized: {new Date(selectedNode.created_at).toLocaleString()}
                            </p>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Bottom Legend */}
            {!selectedNode && (
                <div className="absolute bottom-6 left-6 z-10 flex gap-6">
                    <LegendItem color="#FCD34D" label="L1 Gems" />
                    <LegendItem color="#818CF8" label="L4 Sovereign" />
                    <LegendItem color="#2DD4BF" label="L3 Semantic" />
                    <LegendItem color="#94A3B8" label="L2 Kinetic" />
                </div>
            )}
        </div>
    );
};

const LegendItem = ({ color, label }: { color: string; label: string }) => (
    <div className="flex items-center gap-2">
        <div className="w-2 h-2 rounded-full" style={{ backgroundColor: color, boxShadow: `0 0 10px ${color}` }} />
        <span className="text-[9px] font-mono text-gray-500 uppercase tracking-widest">{label}</span>
    </div>
);

export default MemoryPalacePage;
