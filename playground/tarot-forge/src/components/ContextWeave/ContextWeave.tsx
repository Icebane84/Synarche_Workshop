import React, { useEffect, useState } from 'react';
import './ContextWeave.css';

interface ContextNode {
    id: string;
    label: string;
    x: number;
    y: number;
    type: 'core' | 'context' | 'inference';
    connections: string[];
}

export const ContextWeave: React.FC = () => {
    const [granularity, setGranularity] = useState(3);
    const [depth, setDepth] = useState(2);
    const [nodes, setNodes] = useState<ContextNode[]>([]);
    const [isWeaving, setIsWeaving] = useState(false);

    // Simulate Weaving Process
    useEffect(() => {
        if (!isWeaving) return;

        const generateNodes = () => {
            const newNodes: ContextNode[] = [];
            // Core Node
            newNodes.push({
                id: 'core',
                label: 'TARGET CONCEPT',
                x: 50,
                y: 50,
                type: 'core',
                connections: [],
            });

            // Generate Context Nodes based on Granularity
            const count = granularity * 3;
            for (let i = 0; i < count; i++) {
                const angle = (i / count) * 2 * Math.PI;
                const radius = 30; // %
                newNodes.push({
                    id: `ctx_${i}`,
                    label: `CTX-${i}`,
                    x: 50 + radius * Math.cos(angle),
                    y: 50 + radius * Math.sin(angle),
                    type: 'context',
                    connections: ['core'],
                });
            }

            // Generate Inference Nodes based on Depth
            if (depth > 1) {
                const infCount = depth * 2;
                for (let i = 0; i < infCount; i++) {
                    const angle = (i / infCount) * 2 * Math.PI + 0.5;
                    const radius = 45; // %
                    newNodes.push({
                        id: `inf_${i}`,
                        label: `INF-${i}`,
                        x: 50 + radius * Math.cos(angle),
                        y: 50 + radius * Math.sin(angle),
                        type: 'inference',
                        connections: [`ctx_${i % count}`], // Connect to context
                    });
                }
            }

            setNodes(newNodes);
            setIsWeaving(false);
        };

        const timer = setTimeout(generateNodes, 800);
        return () => clearTimeout(timer);
    }, [isWeaving, granularity, depth]);

    // Initial Weave
    useEffect(() => {
        setIsWeaving(true);
    }, []);

    // SVG Line Generator
    const renderConnections = () => {
        return nodes.flatMap((node) =>
            node.connections.map((targetId) => {
                const target = nodes.find((n) => n.id === targetId);
                if (!target) return null;
                return (
                    <line
                        key={`${node.id}-${target.id}`}
                        x1={`${node.x}%`}
                        y1={`${node.y}%`}
                        x2={`${target.x}%`}
                        y2={`${target.y}%`}
                        stroke="rgba(0, 255, 242, 0.3)"
                        strokeWidth="1"
                    />
                );
            })
        );
    };

    return (
        <div className="context-weave-container">
            <div className="weave-viz">
                <svg className="weave-svg">
                    {renderConnections()}
                    {nodes.map((node) => (
                        <circle
                            key={node.id}
                            cx={`${node.x}%`}
                            cy={`${node.y}%`}
                            r={node.type === 'core' ? 6 : 4}
                            className={`node node-${node.type}`}
                        />
                    ))}
                    {nodes.map((node) => (
                        <text
                            key={`lbl-${node.id}`}
                            x={`${node.x}%`}
                            y={`${node.y + 2}%`}
                            className="node-label"
                            textAnchor="middle"
                        >
                            {node.label}
                        </text>
                    ))}
                </svg>
                {isWeaving && <div className="weaving-overlay">WEAVING CONTEXT...</div>}
            </div>

            <div className="weave-controls">
                <div className="control-group">
                    <label>Context Granularity ({granularity})</label>
                    <input
                        type="range"
                        min="1"
                        max="10"
                        value={granularity}
                        onChange={(e) => {
                            setGranularity(Number(e.target.value));
                            setIsWeaving(true);
                        }}
                    />
                </div>
                <div className="control-group">
                    <label>Search Depth ({depth})</label>
                    <input
                        type="range"
                        min="1"
                        max="5"
                        value={depth}
                        onChange={(e) => {
                            setDepth(Number(e.target.value));
                            setIsWeaving(true);
                        }}
                    />
                </div>
                <div className="control-metrics">
                    <div className="metric">
                        <span className="val">{nodes.length}</span>
                        <span className="lbl">NODES</span>
                    </div>
                    <div className="metric">
                        <span className="val">{nodes.length - 1}</span>
                        <span className="lbl">LINKS</span>
                    </div>
                    <div className="metric">
                        <span className="val">ESF-ALPHA</span>
                        <span className="lbl">SIGNAL</span>
                    </div>
                </div>
            </div>
        </div>
    );
};
