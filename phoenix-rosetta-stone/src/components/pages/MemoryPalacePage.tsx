import { AnimatePresence, motion } from "framer-motion";
import { Database, Maximize2, Minimize2, Search, Sparkles, Swords, X, Zap } from "lucide-react";
import React, { useEffect, useMemo, useRef, useState } from "react";
import ForceGraph3D from "react-force-graph-3d";
import { useSensoryResonance } from "../../hooks/useSensoryResonance";
import { MemoryNode, useMemoryStore } from "../../store/memoryStore";

// Graph Ingestion Database and Engine
import graphDb from "../../data/adjacency_matrix.json";
import { GraphCombatEngine, type BattleState } from "../../engine/GraphCombatEngine";

/**
 * Memory Palace [OMEGA v15.0]
 * 3D Kinetic Force Graph Visualization of the Cognitive Substrate.
 * Upgraded with the Ontological Graph-Wielding Autobattler Mode (Ashen Oath).
 */

interface GraphNode extends MemoryNode {
    val: number;
    color: string;
    x?: number;
    y?: number;
    z?: number;
    opacity?: number;
}

const getLayerLabel = (layer: number) => {
    switch (layer) {
        case 1:
            return { text: "L1 Gem", color: "border-amber-400/50 text-amber-300" };
        case 2:
            return { text: "L2 Kinetic", color: "border-cyan-400/50 text-cyan-300" };
        case 3:
            return { text: "L3 Semantic", color: "border-indigo-400/50 text-indigo-300" };
        case 4:
            return { text: "L4 Sovereign", color: "border-emerald-400/50 text-emerald-300" };
        case 5:
            return { text: "L5 Meta", color: "border-red-400/50 text-red-300" };
        default:
            return { text: "Unknown Layer", color: "border-gray-400/50 text-gray-300" };
    }
};

const LegendItem = ({ color, label }: { color: string; label: string }) => (
    <div className="flex items-center gap-2">
        <div className="w-2 h-2 rounded-full" style={{ backgroundColor: color, boxShadow: `0 0 10px ${color}` }} />
        <span className="text-[9px] font-mono text-gray-500 uppercase tracking-widest">{label}</span>
    </div>
);

/**
 * Builds the graph data for the default "Spectator" mode.
 * It maps memory nodes to visual properties like color and size.
 */
const buildSpectatorGraphData = (storeNodes: MemoryNode[], storeLinks: { source: any; target: any }[]) => {
    // 1. Convert graphDb.nodes to MemoryNode format
    const rawWlfNodes: any[] = Array.isArray(graphDb.nodes) ? graphDb.nodes : Object.values(graphDb.nodes);
    const wlfNodes: MemoryNode[] = rawWlfNodes.map((n: any) => {
        let layer = 2; // Default Kinetic
        if (n.label === "CAN") layer = 1;
        else if (n.label === "Cosmology" || n.label === "Event") layer = 5;
        else if (n.label === "Faction" || n.label === "Location") layer = 4;
        else if (n.label === "Ability" || n.label === "Artifact") layer = 3;

        return {
            id: String(n.id),
            content: `${n.name} [${n.label}]`,
            domain: n.label || "WLF Canon",
            layer,
            tags: n.aliases || [n.label],
            activation: 0.8,
            created_at: new Date().toISOString(),
        };
    });

    // Combine store nodes and WLF nodes, deduping by id
    const allNodesMap = new Map<string, MemoryNode>();
    wlfNodes.forEach((n) => allNodesMap.set(String(n.id), n));
    storeNodes.forEach((n) => allNodesMap.set(String(n.id), n));
    const combinedNodes = Array.from(allNodesMap.values());

    // Combine store links and graphDb.edges
    const wlfLinks = (graphDb.edges || []).map((e: any) => ({
        source: String(e.source),
        target: String(e.target),
    }));
    const combinedLinks = [...storeLinks, ...wlfLinks];

    const nodeIds = new Set(combinedNodes.map((n) => String(n.id)));
    const validLinks = combinedLinks.filter(
        (l) => nodeIds.has(String(typeof l.source === 'object' ? l.source.id : l.source)) &&
               nodeIds.has(String(typeof l.target === 'object' ? l.target.id : l.target))
    );

    return {
        nodes: combinedNodes.map((n) => {
            let nodeColor = "#94A3B8";
            if (n.domain === "Character") nodeColor = "#06B6D4"; // Cyan
            else if (n.domain === "Artifact" || n.domain === "Relic") nodeColor = "#A78BFA"; // Purple
            else if (n.domain === "Ability" || n.domain === "Talent") nodeColor = "#10B981"; // Emerald
            else if (n.domain === "Enemy") nodeColor = "#EF4444"; // Red
            else if (n.domain === "Location" || n.domain === "Zone") nodeColor = "#F59E0B"; // Amber
            else if (n.domain === "CAN") nodeColor = "#FCD34D"; // Gold
            else if (n.domain === "Faction") nodeColor = "#818CF8"; // Indigo
            else if (n.domain === "Cosmology") nodeColor = "#EC4899"; // Pink
            else if (n.domain === "Event") nodeColor = "#3B82F6"; // Blue
            else if (n.domain === "Concept" || n.domain === "System" || n.domain === "Phenomenon") nodeColor = "#34D399"; // Mint
            else if (n.domain === "Codebase") {
                if (n.tags.includes("dir:components") || n.tags.includes("dir:ui")) nodeColor = "#06B6D4";
                else if (n.tags.includes("dir:store") || n.tags.includes("dir:state")) nodeColor = "#10B981";
                else if (n.tags.includes("dir:services") || n.tags.includes("dir:core") || n.tags.includes("dir:hooks")) nodeColor = "#6366F1";
                else nodeColor = "#F59E0B";
            } else {
                nodeColor =
                    n.layer === 1
                        ? "#FCD34D"
                        : n.layer === 4
                          ? "#818CF8"
                          : n.layer === 3
                            ? "#2DD4BF"
                            : "#94A3B8";
            }
            return {
                ...n,
                val: (n.activation || 0.8) * 10 + 4,
                color: nodeColor,
            };
        }),
        links: validLinks,
    };
};

/**
 * Builds the graph data for the "Ashen Arena" battle mode.
 * It uses a static JSON graph and applies dynamic visual states from the combat engine.
 */
const buildBattleGraphData = (battleState: BattleState | null) => {
    const activePulsing = battleState?.activePulsingNodes || [];
    const activeGlows = battleState?.activeGlowLinks || [];

    const rawNodes: any[] = Array.isArray(graphDb.nodes) ? graphDb.nodes : Object.values(graphDb.nodes);
    const compiledNodes = rawNodes.map((n: any) => {
        let color = "#94A3B8";
        if (n.label === "Character") color = "#06B6D4"; // Cyan
        else if (n.label === "Artifact" || n.label === "Relic") color = "#A78BFA"; // Purple
        else if (n.label === "Ability" || n.label === "Talent") color = "#10B981"; // Emerald
        else if (n.label === "Enemy") color = "#EF4444"; // Red
        else if (n.label === "Location" || n.label === "Zone") color = "#F59E0B"; // Amber
        else if (n.label === "CAN") color = "#FCD34D"; // Gold
        else if (n.label === "Faction") color = "#818CF8"; // Indigo
        else if (n.label === "Cosmology") color = "#EC4899"; // Pink
        else if (n.label === "Event") color = "#3B82F6"; // Blue
        else if (n.label === "Concept" || n.label === "System" || n.label === "Phenomenon") color = "#34D399"; // Mint

        const isPulsing = activePulsing.includes(n.id);
        return {
            id: n.id,
            content: `${n.name} [${n.label}]`,
            domain: n.label,
            layer: 1,
            tags: n.aliases || [],
            val: isPulsing ? 25 : 12,
            color: isPulsing ? "#FFFFFF" : color,
            activation: isPulsing ? 1 : 0.4,
            created_at: new Date().toISOString(),
        };
    });

    const validNodeIds = new Set(compiledNodes.map((n: any) => String(n.id)));
    const compiledLinks = (graphDb.edges || [])
        .filter((e: any) => validNodeIds.has(String(e.source)) && validNodeIds.has(String(e.target)))
        .map((e: any, index: number) => {
            const isGlowing = activeGlows.some(
                (gl) =>
                    (gl.source === e.source && gl.target === e.target) ||
                    (gl.source === e.target && gl.target === e.source),
            );
            return {
                id: `edge-${index}`,
                source: e.source,
                target: e.target,
                label: e.relation,
                weight: isGlowing ? 4 : 1,
                color: isGlowing ? "#FFFFFF" : "rgba(255, 255, 255, 0.08)",
            };
        });

    return { nodes: compiledNodes, links: compiledLinks };
};

const MemoryPalacePage: React.FC = () => {
    const nodes = useMemoryStore((state) => state.nodes);
    const links = useMemoryStore((state) => state.links);
    const updateNode = useMemoryStore((state) => state.updateNode);
    const gemifyMemory = useMemoryStore((state) => state.gemifyMemory);
    const fetchMemories = useMemoryStore((state) => state.fetchMemories);
    const resonance = useSensoryResonance();
    const graphRef = useRef<any>(undefined);

    const [selectedNode, setSelectedNode] = useState<any>(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [isFullscreen, setIsFullscreen] = useState(false);

    // Battle Simulator State
    const [isBattleMode, setIsBattleMode] = useState(false);
    const [battleState, setBattleState] = useState<BattleState | null>(null);
    const engineRef = useRef<GraphCombatEngine | null>(null);

    useEffect(() => {
        void fetchMemories();
    }, [fetchMemories]);

    // Handle Battle Engine lifecycle
    useEffect(() => {
        if (isBattleMode) {
            setSelectedNode(null);
            const engine = new GraphCombatEngine(
                (updatedState) => {
                    setBattleState(updatedState);
                },
                ["talent-eternal-ember", "talent-alerion-reflexes"],
            ); // Mock unlocked talents for demo

            engineRef.current = engine;
            engine.start();
        } else {
            engineRef.current?.stop();
            engineRef.current = null;
            setBattleState(null);
        }

        return () => {
            engineRef.current?.stop();
        };
    }, [isBattleMode]);

    // Graph Settings for Spectator Mode
    const spectatorData = useMemo(() => buildSpectatorGraphData(nodes, links), [nodes, links]);

    // Graph Settings for Battle Mode (Compiled from adjacency_matrix.json)
    const battleData = useMemo(() => buildBattleGraphData(battleState), [battleState]);

    const handleNodeClick = (node: object) => {
        const gNode = node as GraphNode;
        setSelectedNode(gNode);
        if (graphRef.current && gNode.x !== undefined && gNode.y !== undefined && gNode.z !== undefined) {
            const distance = 40;
            const distRatio = 1 + distance / Math.hypot(gNode.x, gNode.y, gNode.z);

            graphRef.current.cameraPosition(
                { x: gNode.x * distRatio, y: gNode.y * distRatio, z: gNode.z * distRatio },
                gNode,
                3000,
            );
        }
    };

    const filteredData = useMemo(() => {
        if (!searchQuery) return spectatorData;
        const lower = searchQuery.toLowerCase();
        return {
            nodes: spectatorData.nodes.map((n) => ({
                ...n,
                opacity: n.content.toLowerCase().includes(lower) || n.domain.toLowerCase().includes(lower) ? 1 : 0.1,
            })),
            links: spectatorData.links,
        };
    }, [spectatorData, searchQuery]);

    const activeGraphData = isBattleMode ? battleData : filteredData;

    // Battle Actions
    const handleTap = () => engineRef.current?.triggerTap();
    const handleGarrettSkill = () => engineRef.current?.triggerGroundingCommand();
    const handleSerafinaSkill = () => engineRef.current?.triggerWhispersOfTheDawn();
    const handleKaelenSkill = () => engineRef.current?.triggerInwardInquisition();

    const handleGemify = () => {
        if (!selectedNode) return;

        // Update the node to become a Layer 1 Gem
        void gemifyMemory(selectedNode.id);
        if (typeof updateNode === 'function') {
            updateNode(selectedNode.id, { layer: 1 });
        }
        setSelectedNode(null); // Close the panel after action
    };

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
                    {isBattleMode ? "Ashen Arena" : "Memory Palace"}
                </motion.h2>
                <div className="flex items-center gap-4">
                    <p className="text-[10px] font-mono text-cyan-500/60 tracking-widest uppercase">
                        {isBattleMode ? "Ontological Ingestion Live-Combat" : "Kinetic Force Projection [Axion v1.0]"}
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
                {/* Battle Toggle Button */}
                <button
                    onClick={() => setIsBattleMode(!isBattleMode)}
                    className={`px-3 py-1.5 flex items-center gap-2 border font-mono text-[10px] rounded transition-all cursor-pointer z-30 ${
                        isBattleMode
                            ? "bg-red-500/10 border-red-500/40 text-red-400 hover:bg-red-500/20"
                            : "bg-white/5 border-white/10 text-white/70 hover:bg-white/10"
                    }`}
                >
                    <Swords size={12} />
                    {isBattleMode ? "DISCONNECT BATTLE" : "IGNITE ARENA"}
                </button>

                {!isBattleMode && (
                    <div className="glass-panel px-3 py-1.5 flex items-center gap-2 bg-black/40 backdrop-blur-md border-white/5">
                        <Search size={14} className="text-gray-500" />
                        <input
                            type="text"
                            placeholder="SEARCH MEMORY..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="bg-transparent text-[10px] font-mono text-white focus:outline-none w-32 border-none"
                        />
                    </div>
                )}

                <button
                    onClick={() => setIsFullscreen(!isFullscreen)}
                    className="p-2 glass-panel hover:bg-white/5 text-gray-400 hover:text-white transition-all z-30"
                >
                    {isFullscreen ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
                </button>
            </div>

            {/* Main Graph View */}
            <div className="flex-1 cursor-crosshair">
                <ForceGraph3D
                    ref={graphRef}
                    graphData={activeGraphData}
                    nodeLabel={(node: object) =>
                        `<div class="p-2 bg-black/85 border border-white/10 text-xs font-mono rounded shadow-lg text-white">${(node as GraphNode).content}</div>`
                    }
                    nodeColor="color"
                    nodeVal="val"
                    linkWidth="weight"
                    linkColor="color"
                    backgroundColor="#000000"
                    onNodeClick={handleNodeClick}
                    nodeOpacity={0.95}
                    enableNodeDrag={false}
                />
            </div>

            {/* Battle Overlay HUD */}
            {isBattleMode && battleState && (
                <div className="absolute bottom-6 right-6 w-96 bg-black/85 backdrop-blur-lg border border-white/10 rounded-xl p-5 flex flex-col gap-4 z-30 shadow-2xl text-xs font-mono">
                    <div className="flex justify-between items-center border-b border-white/5 pb-2">
                        <span className="text-red-400 font-bold tracking-widest text-[10px]">ACTIVE COMBAT ENGINE</span>
                        <span className="text-white/40">Stage Wins: {battleState.victoryCount}</span>
                    </div>

                    {/* Adversary details */}
                    <div className="space-y-1.5">
                        <div className="flex justify-between text-white/80 font-bold">
                            <span>Target: {battleState.enemyName}</span>
                            <span>
                                {battleState.enemyHealth} / {battleState.enemyMaxHealth}
                            </span>
                        </div>
                        <div className="w-full h-2 bg-white/5 rounded border border-white/10 overflow-hidden">
                            <div
                                className="h-full bg-red-600 transition-all duration-300 shadow-[0_0_8px_rgba(239,68,68,0.4)]"
                                style={{
                                    width: `${Math.max(0, (battleState.enemyHealth / battleState.enemyMaxHealth) * 100)}%`,
                                }}
                            />
                        </div>
                        <div className="flex justify-between text-[9px] text-white/40">
                            <span>Status: {battleState.isStunned ? "STUNNED" : "ENGAGED"}</span>
                            {battleState.exposedStacks > 0 && (
                                <span className="text-amber-300">Exposed stacks: x{battleState.exposedStacks}</span>
                            )}
                        </div>
                    </div>

                    {/* Shared Inner Flame */}
                    <div className="space-y-1.5 border-t border-white/5 pt-3">
                        <div className="flex justify-between text-white/80 font-bold">
                            <span className="text-yellow-400">Shared Inner Flame</span>
                            <span>{battleState.innerFlame} / 100</span>
                        </div>
                        <div className="w-full h-2 bg-white/5 rounded border border-white/10 overflow-hidden">
                            <div
                                className={`h-full transition-all duration-300 ${battleState.innerFlame < 40 ? "bg-purple-600 shadow-[0_0_8px_rgba(128,90,213,0.5)]" : "bg-yellow-500 shadow-[0_0_8px_rgba(234,179,8,0.4)]"}`}
                                style={{ width: `${battleState.innerFlame}%` }}
                            />
                        </div>
                    </div>

                    {/* Battle Log */}
                    <div className="h-20 overflow-y-auto scrollbar-thin border-t border-white/5 pt-3 mt-2 text-[10px] text-white/50 space-y-1.5">
                        {(battleState.combatLog || battleState.log || []).slice(-5).map((log: string, i: number) => (
                            <p
                                key={i}
                                className="leading-snug animate-fade-in-up"
                                dangerouslySetInnerHTML={{ __html: log }}
                            />
                        ))}
                    </div>

                    {/* Player Actions */}
                    <div className="grid grid-cols-4 gap-2 pt-3 border-t border-white/5">
                        <button
                            onClick={handleTap}
                            className="p-2 border border-cyan-500/30 hover:border-cyan-500 bg-cyan-500/5 text-cyan-400 hover:text-white rounded text-[8px] font-bold tracking-tight text-center cursor-pointer transition-all"
                        >
                            TAP
                        </button>
                        <button
                            onClick={handleKaelenSkill}
                            disabled={battleState.innerFlame < 50}
                            className="p-2 border border-red-500/30 hover:border-red-500 bg-red-500/5 text-red-400 hover:text-white rounded text-[8px] font-bold tracking-tight text-center cursor-pointer transition-all disabled:opacity-30 disabled:cursor-not-allowed"
                        >
                            KAELEN ATK
                        </button>
                        <button
                            onClick={handleSerafinaSkill}
                            disabled={battleState.innerFlame <= 0}
                            className="p-2 border border-yellow-500/30 hover:border-yellow-500 bg-yellow-500/5 text-yellow-400 hover:text-white rounded text-[8px] font-bold tracking-tight text-center cursor-pointer transition-all disabled:opacity-30 disabled:cursor-not-allowed"
                        >
                            SERAFINA HEAL
                        </button>
                        <button
                            onClick={handleGarrettSkill}
                            disabled={battleState.innerFlame <= 0 || battleState.isStunned}
                            className="p-2 border border-blue-500/30 hover:border-blue-500 bg-blue-500/5 text-blue-400 hover:text-white rounded text-[8px] font-bold tracking-tight text-center cursor-pointer transition-all disabled:opacity-30 disabled:cursor-not-allowed"
                        >
                            GARRETT STUN
                        </button>
                    </div>
                </div>
            )}

            {/* Interactive WLF Codex & Relational Knowledge Inspector Panel */}
            <AnimatePresence>
                {selectedNode && (
                    <motion.div
                        initial={{ x: "100%" }}
                        animate={{ x: 0 }}
                        exit={{ x: "100%" }}
                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                        className="absolute top-0 right-0 bottom-0 w-96 glass-panel border-l border-cyan-500/30 bg-black/85 backdrop-blur-3xl z-20 p-6 flex flex-col gap-5 overflow-y-auto scrollbar-thin shadow-[-10px_0_30px_rgba(6,182,212,0.15)]"
                    >
                        {/* Header */}
                        <div className="flex justify-between items-start border-b border-white/10 pb-4">
                            <div className="flex items-center gap-2.5">
                                <Sparkles size={18} className="text-cyan-400 animate-pulse" />
                                <div>
                                    <h2 className="text-sm font-mono font-bold text-white tracking-wide uppercase">
                                        {selectedNode.content || selectedNode.name || `Node #${selectedNode.id}`}
                                    </h2>
                                    <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-widest font-semibold">
                                        {selectedNode.domain || "Knowledge Node"} • ID: {selectedNode.id}
                                    </span>
                                </div>
                            </div>
                            <button
                                onClick={() => setSelectedNode(null)}
                                className="text-gray-400 hover:text-white transition-all p-1 hover:bg-white/10 rounded-full"
                            >
                                <X size={18} />
                            </button>
                        </div>

                        {/* OMEGA Layer & Category Badges */}
                        <div className="space-y-1.5">
                            <h3 className="text-[10px] font-bold font-mono text-gray-400 uppercase tracking-wider">
                                Classification & OMEGA Layer
                            </h3>
                            <div className="flex flex-wrap gap-2 items-center">
                                {(() => {
                                    const lInfo = getLayerLabel(selectedNode.layer || 1);
                                    return (
                                        <span
                                            className={`px-3 py-1 border rounded-md text-[10px] font-mono uppercase tracking-wider ${lInfo.color}`}
                                        >
                                            {lInfo.text}
                                        </span>
                                    );
                                })()}

                                {selectedNode.domain && (
                                    <span className="px-2.5 py-1 bg-cyan-500/10 border border-cyan-500/30 rounded-md text-[10px] font-mono text-cyan-300 font-bold uppercase">
                                        🏷️ {selectedNode.domain}
                                    </span>
                                )}
                            </div>
                        </div>

                        {/* Raw Canonical Properties Sheet */}
                        {(() => {
                            const rawGraphNode = (graphDb.nodes as any[])?.find((n: any) => n.id === selectedNode.id);
                            const props = rawGraphNode?.properties;
                            if (!props || Object.keys(props).length === 0) return null;

                            return (
                                <div className="space-y-2 border-t border-white/5 pt-3">
                                    <h3 className="text-[10px] font-bold font-mono text-cyan-300 uppercase tracking-wider">
                                        📜 WLF Canonical Properties & Lore
                                    </h3>
                                    <div className="bg-black/60 border border-white/10 rounded-lg p-3 space-y-2 text-[11px] font-mono">
                                        {Object.entries(props).map(([k, v]) => (
                                            <div key={k} className="flex flex-col gap-0.5 border-b border-white/5 pb-1.5 last:border-0 last:pb-0">
                                                <span className="text-[9px] text-gray-400 uppercase font-bold tracking-wider">{k}</span>
                                                <span className="text-gray-200 leading-snug">{String(v)}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            );
                        })()}

                        {/* Connected Relational Nodes Sheet */}
                        {(() => {
                            const rawEdges = (graphDb.edges as any[]) || [];
                            const connected = rawEdges.filter(
                                (e: any) => e.source === selectedNode.id || e.target === selectedNode.id
                            );

                            if (connected.length === 0) return null;

                            return (
                                <div className="space-y-2 border-t border-white/5 pt-3">
                                    <div className="flex justify-between items-center">
                                        <h3 className="text-[10px] font-bold font-mono text-yellow-400 uppercase tracking-wider flex items-center gap-1.5">
                                            🔗 Synaptic Links ({connected.length})
                                        </h3>
                                        <span className="text-[9px] font-mono text-gray-500">Click to Inspect</span>
                                    </div>
                                    <div className="max-h-48 overflow-y-auto space-y-1.5 pr-1 scrollbar-thin">
                                        {connected.map((edge: any, idx: number) => {
                                            const isSource = edge.source === selectedNode.id;
                                            const targetId = isSource ? edge.target : edge.source;
                                            const targetNode = (graphDb.nodes as any[])?.find((n: any) => n.id === targetId);
                                            const targetName = targetNode?.name || targetId;
                                            const targetLabel = targetNode?.label || "Node";

                                            return (
                                                <button
                                                    key={idx}
                                                    onClick={() => {
                                                        const compiledTarget = activeGraphData.nodes.find((n: any) => n.id === targetId);
                                                        if (compiledTarget) handleNodeClick(compiledTarget);
                                                    }}
                                                    className="w-full text-left p-2 bg-white/5 hover:bg-cyan-500/20 border border-white/10 hover:border-cyan-500/40 rounded-lg font-mono text-xs transition-all group flex items-center justify-between gap-2"
                                                >
                                                    <div className="flex items-center gap-2 truncate">
                                                        <span className="text-[10px] text-cyan-400 font-bold px-1.5 py-0.5 bg-black/40 rounded border border-cyan-500/20">
                                                            {isSource ? "➡️" : "⬅️"} {edge.relation}
                                                        </span>
                                                        <span className="text-gray-200 group-hover:text-white font-semibold truncate">
                                                            {targetName}
                                                        </span>
                                                    </div>
                                                    <span className="text-[9px] text-gray-500 font-mono shrink-0 uppercase">
                                                        [{targetLabel}]
                                                    </span>
                                                </button>
                                            );
                                        })}
                                    </div>
                                </div>
                            );
                        })()}

                        {/* Activation Score Bar */}
                        <div className="space-y-1.5 border-t border-white/5 pt-3">
                            <div className="flex justify-between text-[10px] font-mono text-gray-400">
                                <span className="font-bold uppercase tracking-wider">Activation Resonance</span>
                                <span>{Math.round((selectedNode.activation || 0.8) * 100)}%</span>
                            </div>
                            <div className="w-full h-2 bg-gray-900 rounded-full overflow-hidden border border-white/10">
                                <div
                                    className="h-full bg-gradient-to-r from-cyan-500 to-amber-400 transition-all duration-500"
                                    style={{ width: `${Math.round((selectedNode.activation || 0.8) * 100)}%` }}
                                />
                            </div>
                        </div>

                        {/* Action: Gemify into L1 Gem */}
                        {selectedNode.layer !== 1 && (
                            <button
                                onClick={handleGemify}
                                className="w-full py-2.5 mt-2 bg-gradient-to-r from-amber-500/20 via-yellow-500/20 to-amber-600/10 border border-amber-500/50 hover:border-amber-400 text-amber-300 hover:text-white rounded-lg font-mono text-xs font-bold tracking-widest text-center cursor-pointer transition-all shadow-[0_0_15px_rgba(252,211,77,0.2)] flex items-center justify-center gap-2"
                            >
                                <Zap size={14} className="text-amber-400" />
                                CRYSTALLIZE INTO L1 GEM
                            </button>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Bottom Legend for 5 OMEGA Layers */}
            {!selectedNode && !isBattleMode && (
                <div className="absolute bottom-6 left-6 z-10 flex gap-5 glass-panel p-3 bg-black/60 backdrop-blur-xl border border-white/10 rounded-xl">
                    <LegendItem color="#FCD34D" label="L1 Gems" />
                    <LegendItem color="#06B6D4" label="L2 Kinetic" />
                    <LegendItem color="#818CF8" label="L3 Semantic" />
                    <LegendItem color="#10B981" label="L4 Sovereign" />
                    <LegendItem color="#F43F5E" label="L5 Meta" />
                </div>
            )}
        </div>
    );
};

export default MemoryPalacePage;
