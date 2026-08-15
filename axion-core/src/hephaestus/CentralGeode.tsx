/**
 * artifact_anchor:
 * - id:
 * - type:
 */
import * as d3 from "d3";
import { useEffect, useRef } from "react";

export interface GeodeNode extends d3.SimulationNodeDatum {
    id: string;
    type: "STAR" | "PLANET" | "MOON";
    coherence: number;
}

export interface GeodeLink extends d3.SimulationLinkDatum<GeodeNode> {
    source: string | GeodeNode;
    target: string | GeodeNode;
    type: "GOVERNS" | "SYNERGY" | "IMPLEMENTS";
}

interface CentralGeodeProps {
    nodes: GeodeNode[];
    links: GeodeLink[];
    globalCoherence: number; // 0.0 to 1.0, dictates ambient glow
    onNodeClick?: (nodeId: string) => void;
}

export default function CentralGeode({ nodes, links, globalCoherence, onNodeClick }: CentralGeodeProps) {
    // React acts as the "Architect", provisioning the DOM Canvas
    const svgRef = useRef<SVGSVGElement>(null);

    // D3 acts as the "Physics Engine", driving force simulations
    useEffect(() => {
        if (!svgRef.current || nodes.length === 0) return;

        const width = 800;
        const height = 600;
        const svg = d3.select(svgRef.current).attr("viewBox", `0 0 ${width} ${height}`);

        // Clear previous render to enforce D3 idempotency
        svg.selectAll("*").remove();

        // Initialize physics simulation
        const simulation = d3
            .forceSimulation<GeodeNode>(nodes)
            .force(
                "link",
                d3
                    .forceLink<GeodeNode, GeodeLink>(links)
                    .id((d) => d.id)
                    .distance(120),
            )
            .force("charge", d3.forceManyBody().strength(-400))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force(
                "collide",
                d3.forceCollide().radius((d) => ((d as GeodeNode).type === "STAR" ? 30 : 15)),
            );

        // Render Links
        const linkSelection = svg
            .append("g")
            .attr("stroke", "#4b5563")
            .attr("stroke-opacity", 0.6)
            .selectAll("line")
            .data(links)
            .join("line")
            .attr("stroke-width", (d) => (d.type === "GOVERNS" ? 2 : 1));

        // Render Nodes
        const nodeSelection = svg
            .append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("circle")
            .data(nodes)
            .join("circle")
            .attr("r", (d) => (d.type === "STAR" ? 14 : d.type === "PLANET" ? 8 : 4))
            .attr("fill", (d) => d3.interpolatePlasma(d.coherence))
            .attr("class", "cursor-crosshair transition-all duration-200 hover:stroke-[3px]")
            .on("click", (event, d) => onNodeClick?.(d.id));

        nodeSelection.append("title").text((d) => `${d.id}\nCoherence: ${d.coherence}`);

        // Physics Tick
        simulation.on("tick", () => {
            linkSelection
                .attr("x1", (d) => (d.source as GeodeNode).x!)
                .attr("y1", (d) => (d.source as GeodeNode).y!)
                .attr("x2", (d) => (d.target as GeodeNode).x!)
                .attr("y2", (d) => (d.target as GeodeNode).y!);

            nodeSelection.attr("cx", (d) => d.x!).attr("cy", (d) => d.y!);
        });

        return () => {
            simulation.stop();
        }; // Clean up on unmount
    }, [nodes, links, onNodeClick]);

    return (
        <div
            className="relative w-full max-w-5xl mx-auto rounded-xl shadow-2xl overflow-hidden bg-[#00001a]"
            style={{ boxShadow: `0 0 40px rgba(119, 181, 254, ${globalCoherence * 0.5})` }}
        >
            <svg ref={svgRef} className="w-full h-auto" />
        </div>
    );
}
