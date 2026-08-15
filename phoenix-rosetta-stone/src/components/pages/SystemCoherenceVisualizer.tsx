import React, { useState, useEffect, useRef, useMemo } from 'react';
import * as d3 from 'd3';
import { graphData, GraphNode, GraphLink } from '../../data/graphData';
import { X, Zap, Loader } from 'lucide-react';
import Tooltip from '../common/Tooltip';
import { dispatchCommand, analyzeSynergyCommand } from '../../services';
import { useCoherenceStore } from '../../store/coherenceStore';
import { useTaskStore } from '../../store/taskStore';

// FIX: Explicitly define d3 simulation properties on SimulationNode.
// The `extends d3.SimulationNodeDatum` was not being correctly resolved, causing
// TypeScript errors that `x`, `y`, `fx`, and `fy` did not exist on the type.
// This ensures the properties are available for the force simulation logic.
interface SimulationNode extends GraphNode {
    index?: number;
    x?: number;
    y?: number;
    vx?: number;
    vy?: number;
    fx?: number | null;
    fy?: number | null;
}
interface SimulationLink extends d3.SimulationLinkDatum<SimulationNode> {
    strength: number;
}

const nodeTypeColors: Record<GraphNode['type'], string> = {
    Document: 'hsl(180, 70%, 60%)', // Cyan
    Concept: 'hsl(260, 80%, 75%)', // Purple
    Principle: 'hsl(50, 90%, 65%)', // Gold
    Aesthetic: 'hsl(320, 80%, 70%)', // Pink
};

const relationshipStrength: Record<GraphLink['relationship'], number> = {
    defines: 0.9,
    mandates: 0.8,
    realizes: 0.7,
    contains: 0.5,
    informs: 0.3,
};

const linkColorScale = d3.scaleSequential(d3.interpolateCool).domain([0.3, 1]);

import { CSEBridgeService } from '../../services/cseBridgeService';

const SystemCoherenceVisualizer: React.FC = () => {
    const svgRef = useRef<SVGSVGElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);
    const linkSelectionRef = useRef<d3.Selection<SVGLineElement, SimulationLink, SVGGElement, unknown> | null>(null);
    const nodeSelectionRef = useRef<d3.Selection<SVGGElement, SimulationNode, SVGGElement, unknown> | null>(null);

    const [selectedNode, setSelectedNode] = useState<SimulationNode | null>(null);
    const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
    const [synergyReport, setSynergyReport] = useState<{ message: string; synergies: string[] } | null>(null);
    const [sfrThreshold, setSfrThreshold] = useState<number>(0);
    const [activeGraph, setActiveGraph] = useState<{ nodes: GraphNode[]; links: GraphLink[] }>(graphData);

    const addNovaSpark = useCoherenceStore((state) => state.addNovaSpark);
    const addTask = useTaskStore((state) => state.addTask);

    // Fetch live Loom Graph from CSE backend
    useEffect(() => {
        let isMounted = true;
        CSEBridgeService.fetchLoomGraph().then((liveData) => {
            if (isMounted && liveData && liveData.nodes.length > 0) {
                const formattedNodes: GraphNode[] = liveData.nodes.map((n) => ({
                    id: n.id,
                    label: n.label,
                    type: (n.type as GraphNode['type']) || 'Document',
                }));
                const formattedLinks: GraphLink[] = liveData.links.map((l) => ({
                    source: l.source,
                    target: l.target,
                    relationship: (l.relationship.toLowerCase() as GraphLink['relationship']) || 'informs',
                }));
                setActiveGraph({ nodes: formattedNodes, links: formattedLinks });
            }
        });
        return () => { isMounted = false; };
    }, []);

    const augmentedLinks = useMemo(
        () =>
            activeGraph.links.map((link) => ({
                ...link,
                strength: relationshipStrength[link.relationship] || 0.1,
            })),
        [activeGraph],
    );

    useEffect(() => {
        if (!svgRef.current || !containerRef.current) return;

        const { width, height } = containerRef.current.getBoundingClientRect();
        const svg = d3.select(svgRef.current).attr('viewBox', [-width / 2, -height / 2, width, height]);

        svg.selectAll('*').remove();

        const nodes: SimulationNode[] = activeGraph.nodes.map((n) => ({ ...n }));
        const links: SimulationLink[] = augmentedLinks.map((l) => ({ ...l }) as unknown as SimulationLink);

        const simulation = d3
            .forceSimulation(nodes)
            .force(
                'link',
                d3
                    .forceLink<SimulationNode, SimulationLink>(links)
                    .id((d) => d.id)
                    .distance(150),
            )
            .force('charge', d3.forceManyBody().strength(-400))
            .force('center', d3.forceCenter(0, 0));

        const defs = svg.append('defs');
        const filter = defs.append('filter').attr('id', 'glow');
        filter.append('feGaussianBlur').attr('stdDeviation', '3.5').attr('result', 'coloredBlur');
        const feMerge = filter.append('feMerge');
        feMerge.append('feMergeNode').attr('in', 'coloredBlur');
        feMerge.append('feMergeNode').attr('in', 'SourceGraphic');

        const g = svg.append('g');

        const link = g
            .append('g')
            // FIX: Explicitly providing generic types to `selectAll` to guide TypeScript's inference,
            // ensuring the resulting selection from `.join()` is correctly typed and assignable.
            .selectAll<SVGLineElement, SimulationLink>('line')
            .data(links)
            .join('line')
            .attr('class', 'synergy-vein')
            .attr('stroke', (d) => linkColorScale(d.strength))
            .style('animation-duration', (d) => `${(2.5 - d.strength * 2).toString()}s`);

        linkSelectionRef.current = link;

        const drag = (simulation: d3.Simulation<SimulationNode, undefined>) => {
            function dragstarted(
                this: SVGGElement,
                event: d3.D3DragEvent<SVGGElement, SimulationNode, SimulationNode>,
                d: SimulationNode,
            ) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }
            function dragged(
                this: SVGGElement,
                event: d3.D3DragEvent<SVGGElement, SimulationNode, SimulationNode>,
                d: SimulationNode,
            ) {
                const nodeRadius = 15; // A bit larger than the circle radius to be safe
                d.fx = Math.max(-width / 2 + nodeRadius, Math.min(width / 2 - nodeRadius, event.x));
                d.fy = Math.max(-height / 2 + nodeRadius, Math.min(height / 2 - nodeRadius, event.y));
            }
            function dragended(
                this: SVGGElement,
                event: d3.D3DragEvent<SVGGElement, SimulationNode, SimulationNode>,
                d: SimulationNode,
            ) {
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }
            return d3
                .drag<SVGGElement, SimulationNode>()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended);
        };

        const node = g
            .append('g')
            // FIX: Explicitly providing generic types to `selectAll` to guide TypeScript's inference,
            // ensuring the resulting selection from `.join()` is correctly typed and assignable.
            .selectAll<SVGGElement, SimulationNode>('g')
            .data(nodes)
            .join('g')
            .attr('cursor', 'pointer')
            .call(drag(simulation));

        nodeSelectionRef.current = node;

        node.append('circle')
            .attr('r', 12)
            .attr('fill', (d) => nodeTypeColors[d.type])
            .style('filter', 'url(#glow)');

        node.append('text')
            .text((d) => d.name)
            .attr('x', 18)
            .attr('y', 5)
            .attr('fill', 'hsl(180, 20%, 90%)')
            .style('font-size', '12px')
            .style('pointer-events', 'none');

        node.on('click', (event, d) => {
            setSelectedNode(d);
            setSynergyReport(null);
        });

        simulation.on('tick', () => {
            link.attr('x1', (d) => ((d.source as SimulationNode).x ?? 0).toString())
                .attr('y1', (d) => ((d.source as SimulationNode).y ?? 0).toString())
                .attr('x2', (d) => ((d.target as SimulationNode).x ?? 0).toString())
                .attr('y2', (d) => ((d.target as SimulationNode).y ?? 0).toString());
            node.attr('transform', (d: SimulationNode) => `translate(${(d.x ?? 0).toString()}, ${(d.y ?? 0).toString()})`);
        });

        const zoom = d3.zoom<SVGSVGElement, unknown>().on('zoom', (event: d3.D3ZoomEvent<SVGSVGElement, unknown>) => {
            g.attr('transform', event.transform.toString());
        });
        svg.call(zoom);

        return () => {
            simulation.stop();
        };
    }, [augmentedLinks]);

    useEffect(() => {
        if (!linkSelectionRef.current) return;

        linkSelectionRef.current
            .transition()
            .duration(300)
            .attr('stroke-opacity', (d) => (d.strength >= sfrThreshold ? 0.4 + d.strength * 0.6 : 0.05));
    }, [sfrThreshold]);

    useEffect(() => {
        if (!nodeSelectionRef.current || !linkSelectionRef.current) return;

        const node = nodeSelectionRef.current;
        const link = linkSelectionRef.current;
        const baseOpacity = (l: SimulationLink) => (l.strength >= sfrThreshold ? 0.4 + l.strength * 0.6 : 0.05);

        node.on('mouseover', (event, d) => {
            link.transition()
                .duration(200)
                .attr('stroke-opacity', (l) => (l.source === d || l.target === d ? 1 : 0.05))
                .attr('stroke', (l) =>
                    l.source === d || l.target === d ? 'hsl(50, 90%, 65%)' : linkColorScale(l.strength),
                );

            node.selectAll('circle')
                .transition()
                .duration(200)
                .attr('r', (n) => (n === d ? 15 : 12));
        }).on('mouseout', () => {
            link.transition()
                .duration(200)
                .attr('stroke-opacity', baseOpacity)
                .attr('stroke', (l) => linkColorScale(l.strength));

            node.selectAll('circle').transition().duration(200).attr('r', 12);
        });
    }, [sfrThreshold]);

    const handleAnalyzeSynergy = async () => {
        if (!selectedNode || isAnalyzing) return;
        setIsAnalyzing(true);
        setSynergyReport(null);
        const result = await dispatchCommand(analyzeSynergyCommand, { artifactId: selectedNode.id });
        if (result.success && result.data) {
            const report = result.data as { message: string; synergies: string[] };
            setSynergyReport(report);
            addNovaSpark(`Synergy analysis complete for artifact: ${selectedNode.name}.`);
            await addTask({
                title: `Investigate Synergy: ${selectedNode.name}`,
                notes: `Synergy analysis found ${report.synergies.length.toString()} potential connections. Further investigation required.`,
                source: 'Synergy Simulator',
                priority: 'Medium',
            });
        } else {
            setSynergyReport({ message: result.message, synergies: [] });
        }
        setIsAnalyzing(false);
    };

    return (
        <div className="h-full w-full relative contain-content" ref={containerRef}>
            <svg ref={svgRef} className="w-full h-full"></svg>

            <div className="absolute top-4 left-4 w-72 p-3 bg-black/50 backdrop-blur-md border border-cyan-500/30 rounded-lg text-cyan-200 animate-fade-in-sm">
                <label
                    htmlFor="sfr-slider"
                    className="text-sm font-light tracking-wider flex justify-between items-center"
                >
                    <span>Synergy Vein Filter</span>
                    <span className="font-mono text-cyan-300">{sfrThreshold.toFixed(1)}</span>
                </label>
                <p className="text-xs text-cyan-400/60 mb-2">Adjust minimum Synergy Flow Rate (SFR) to display.</p>
                <input
                    id="sfr-slider"
                    type="range"
                    min="0"
                    max="0.9"
                    step="0.1"
                    value={sfrThreshold}
                    onChange={(e) => {
                        setSfrThreshold(parseFloat(e.target.value));
                    }}
                    className="w-full h-2 bg-cyan-900/50 rounded-lg appearance-none cursor-pointer range-slider"
                />
            </div>

            {selectedNode && (
                <div className="absolute top-4 right-4 w-96 max-h-[calc(100vh-2rem)] flex flex-col p-4 bg-black/50 backdrop-blur-md border border-cyan-500/30 rounded-lg text-cyan-200 animate-fade-in-sm">
                    <Tooltip label="Close Details">
                        <button
                            onClick={() => {
                                setSelectedNode(null);
                            }}
                            className="absolute top-2 right-2 text-cyan-400/50 hover:text-cyan-200"
                        >
                            <X size={20} />
                        </button>
                    </Tooltip>
                    <h3
                        className="text-xl font-light tracking-wide"
                        style={{ color: nodeTypeColors[selectedNode.type] }}
                    >
                        {selectedNode.name}
                    </h3>
                    <p className="text-sm uppercase tracking-widest text-cyan-400/60 mt-1">{selectedNode.type}</p>
                    <hr className="my-3 border-cyan-500/20" />
                    <div className="overflow-y-auto pr-2 scrollbar-thin">
                        <p className="text-cyan-300/90 mb-4">{selectedNode.description}</p>

                        <Tooltip label="Analyze this artifact for potential synergies with other system components.">
                            <button
                                onClick={() => {
                                    void handleAnalyzeSynergy();
                                }}
                                disabled={isAnalyzing}
                                className="w-full flex items-center justify-center gap-2 px-4 py-2 mb-4 bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-400/30 rounded-md text-cyan-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
                            >
                                {isAnalyzing ? (
                                    <>
                                        <Loader className="w-4 h-4 animate-spin" />
                                        Analyzing...
                                    </>
                                ) : (
                                    <>
                                        <Zap className="w-4 h-4" />
                                        Analyze Synergy
                                    </>
                                )}
                            </button>
                        </Tooltip>

                        {synergyReport && (
                            <div className="animate-fade-in-sm">
                                <h4 className="text-md font-light tracking-wide text-cyan-300 mb-2">
                                    Analysis Report:
                                </h4>
                                <p className="text-xs text-cyan-400/70 italic mb-3">{synergyReport.message}</p>
                                {synergyReport.synergies.length > 0 ? (
                                    <ul className="space-y-3 text-sm">
                                        {synergyReport.synergies.map((synergy, index) => (
                                            <li
                                                key={index}
                                                className="p-2 bg-black/20 border-l-2 border-amber-400/50 text-cyan-300/90"
                                                dangerouslySetInnerHTML={{
                                                    __html: synergy.replace(
                                                        /\*\*(.*?)\*\*/g,
                                                        '<strong class="font-semibold text-amber-300">$1</strong>',
                                                    ),
                                                }}
                                            />
                                        ))}
                                    </ul>
                                ) : synergyReport.synergies.length === 0 && !isAnalyzing ? (
                                    <p className="text-sm p-2 bg-black/20 border-l-2 border-cyan-400/50 text-cyan-300/90">
                                        No indirect synergies found.
                                    </p>
                                ) : null}
                            </div>
                        )}
                    </div>
                </div>
            )}
            <style>{`
        @keyframes fade-in-sm {
            from { opacity: 0; transform: translateX(10px); }
            to { opacity: 1; transform: translateX(0); }
        }
        .animate-fade-in-sm { animation: fade-in-sm 0.3s ease-out forwards; }
        .scrollbar-thin::-webkit-scrollbar { width: 4px; }
        .scrollbar-thin::-webkit-scrollbar-track { background: transparent; }
        .scrollbar-thin::-webkit-scrollbar-thumb { background-color: rgba(0, 255, 255, 0.2); border-radius: 20px; }
        
        @keyframes pulse-vein {
            0%, 100% { stroke-opacity: 0.4; filter: brightness(0.8); }
            50% { stroke-opacity: 1; filter: brightness(1.5); }
        }
        .synergy-vein {
            animation-name: pulse-vein;
            animation-timing-function: ease-in-out;
            animation-iteration-count: infinite;
        }

        .range-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            background: #22d3ee;
            cursor: pointer;
            border-radius: 50%;
            box-shadow: 0 0 8px rgba(34, 211, 238, 0.7);
            margin-top: -7px;
        }
        .range-slider::-moz-range-thumb {
            width: 16px;
            height: 16px;
            background: #22d3ee;
            cursor: pointer;
            border-radius: 50%;
            box-shadow: 0 0 8px rgba(34, 211, 238, 0.7);
        }
      `}</style>
        </div>
    );
};

export default SystemCoherenceVisualizer;
