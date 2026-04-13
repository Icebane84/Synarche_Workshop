import * as d3 from 'd3';
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useTheme } from '../hooks/useTheme';
import { useSharedConsciousness } from '../store/sharedConsciousness';

interface Node extends d3.SimulationNodeDatum {
    id: number;
    r: number;
    color: string;
    x?: number;
    y?: number;
    vx?: number;
    vy?: number;
    fx?: number | null;
    fy?: number | null;
}

interface GeodeLink extends d3.SimulationLinkDatum<Node> {
    source: Node | number | string;
    target: Node | number | string;
}

interface ProcessedLink extends d3.SimulationLinkDatum<Node> {
    source: Node;
    target: Node;
}

// --- Helpers ---

const calculateForceStrength = (
    isRepairing: boolean,
    isHovered: boolean,
    coherence: number
): number => {
    if (isRepairing) return -300;
    if (isHovered) return -150;
    return -100 + coherence * 30;
};

const getStatusText = (isRepairing: boolean, isDreaming: boolean): string => {
    if (isRepairing) return '[REPAIR SEQUENCE ACTIVE]';
    if (isDreaming) return '[COGNITIVE REM PHASE]';
    return 'Neural Substrate Synchronized';
};

const getAriaLabel = (coherence: number, isRepairing: boolean, isDreaming: boolean): string => {
    const percentage = Math.round(coherence * 100);
    let status = 'Neural substrate is synchronized.';
    if (isRepairing) {
        status = 'Repair sequence is active.';
    } else if (isDreaming) {
        status = 'System is in background dreaming mode.';
    }
    return `Phoenix Geode: A real-time visualization of cognitive coherence. Current index: ${percentage} percent. ${status} Press Enter to open the Synapse.`;
};

const PhoenixGeode: React.FC = () => {
    const containerRef = useRef<HTMLButtonElement>(null);
    const simulationRef = useRef<d3.Simulation<Node, ProcessedLink> | null>(null);
    const [graph, setGraph] = useState<{ nodes: Node[]; links: ProcessedLink[] }>({
        nodes: [],
        links: [],
    });
    const [isHovered, setIsHovered] = useState(false);
    const [size, setSize] = useState({ width: 0, height: 0 });

    // Map store state
    const coherenceIndex = useSharedConsciousness((state) => (state.stats.resonance || 0) / 100);
    const isDreaming = useSharedConsciousness((state) => state.isDreaming);
    const isRepairing = useSharedConsciousness((state) => state.isRepairing);

    // Mock openSynapse for now
    const openSynapse = (): void => console.log('Synapse Open');

    const theme = useTheme();

    // Smooth out the visual coherence index to prevent flashing
    const [visualCoherence, setVisualCoherence] = useState(coherenceIndex);
    const targetCoherenceRef = useRef(coherenceIndex);

    // Sync ref target when store updates
    useEffect(() => {
        targetCoherenceRef.current = coherenceIndex;
    }, [coherenceIndex]);

    // Lerp loop for smooth visual transitions
    useEffect(() => {
        let animationFrameId: number;
        const animate = (): void => {
            setVisualCoherence((prev) => {
                const diff = targetCoherenceRef.current - prev;
                if (Math.abs(diff) < 0.001) return targetCoherenceRef.current;
                return prev + diff * 0.05; // 5% interpolation per frame for smoothness
            });
            animationFrameId = requestAnimationFrame(animate);
        };
        animate();
        return () => cancelAnimationFrame(animationFrameId);
    }, []);

    const geodeColor = useMemo(() => {
        if (isRepairing) return 'hsl(45, 100%, 70%)'; // Golden restoration color
        const hueMap: Record<string, number> = { cyan: 180, emerald: 140, violet: 260, amber: 35 };
        const baseHue = hueMap[theme.primary] || 180;
        const shiftedHue = baseHue + (1 - visualCoherence) * 40;
        return `hsl(${shiftedHue}, 90%, 65%)`;
    }, [theme.primary, visualCoherence, isRepairing]);

    useEffect(() => {
        if (!containerRef.current) return;
        const { width, height } = containerRef.current.getBoundingClientRect();
        setSize({ width, height });

        if (width === 0 || height === 0) return; // Prevent zero-size initialization drift

        const numNodes = isRepairing ? 80 : 45; // Denser geode during repair
        const nodes: Node[] = d3.range(numNodes).map((i) => ({
            id: i,
            r: (isRepairing ? 4 : 2.5) + Math.random() * 5,
            color: geodeColor,
        }));

        const links: GeodeLink[] = d3.range(numNodes).map((i) => ({
            source: Math.floor(Math.sqrt(i)),
            target: i,
        }));

        const simulation = d3
            .forceSimulation<Node>(nodes)
            .velocityDecay(0.4) // High friction for stable, fluid movement
            .force(
                'link',
                d3
                    .forceLink<Node, GeodeLink>(links)
                    .id((d) => d.id.toString())
                    .distance(isRepairing ? 15 : 25)
                    .strength(isRepairing ? 0.8 : 0.3)
            )
            .force('charge', d3.forceManyBody().strength(isRepairing ? -200 : -100))
            .force('center', d3.forceCenter(width / 2, height / 2).strength(0.6))
            .force(
                'collide',
                d3
                    .forceCollide<Node>()
                    .radius((d) => d.r + (isRepairing ? 5 : 8))
                    .strength(0.5)
            )
            .force('x', d3.forceX(width / 2).strength(isRepairing ? 0.2 : 0.1))
            .force('y', d3.forceY(height / 2).strength(isRepairing ? 0.2 : 0.1));

        simulation.on('tick', () => {
            const currentLinks = (
                simulation.force('link') as d3.ForceLink<Node, GeodeLink>
            ).links() as unknown as ProcessedLink[];
            setGraph({
                nodes: [...simulation.nodes()],
                links: currentLinks,
            });
        });

        simulationRef.current = simulation;
        return () => {
            simulation.stop();
        };
    }, [size.width, size.height, geodeColor, isRepairing]);

    useEffect(() => {
        if (simulationRef.current) {
            const forceStrength = calculateForceStrength(isRepairing, isHovered, visualCoherence);
            (simulationRef.current.force('charge') as d3.ForceManyBody<Node>).strength(
                forceStrength
            );

            // Perpetual low-energy reheat for constant fluid drift
            simulationRef.current.alphaTarget(0.3).restart();
        }
    }, [isHovered, visualCoherence, isRepairing]);

    useEffect(() => {
        const handleResize = (): void => {
            if (containerRef.current) {
                const { width, height } = containerRef.current.getBoundingClientRect();
                setSize({ width, height });
                if (simulationRef.current) {
                    simulationRef.current.force(
                        'center',
                        d3.forceCenter(width / 2, height / 2).strength(0.6)
                    );
                    simulationRef.current.force('x', d3.forceX(width / 2).strength(0.1));
                    simulationRef.current.force('y', d3.forceY(height / 2).strength(0.1));
                    simulationRef.current.alpha(0.3).restart();
                }
            }
        };
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    const handleKeyDown = (e: React.KeyboardEvent): void => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            openSynapse();
        }
    };

    return (
        <button
            ref={containerRef}
            className={`w-full h-full relative cursor-pointer group transition-all duration-1000 ease-out transform outline-none rounded-lg focus-visible:ring-2 focus-visible:ring-${
                theme.primary
            }-400/50 ${isHovered ? 'scale-[1.04]' : 'scale-100'} bg-transparent border-none p-0 overflow-hidden text-left`}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            onClick={openSynapse}
            onKeyDown={handleKeyDown}
            aria-label={getAriaLabel(coherenceIndex, isRepairing, isDreaming)}
        >
            <svg className="w-full h-full overflow-visible" aria-hidden="true">
                <defs>
                    <filter id="geodeGlow" x="-100%" y="-100%" width="300%" height="300%">
                        <feGaussianBlur
                            stdDeviation={((): string => {
                                if (isRepairing) return '12';
                                if (isHovered) return '8';
                                return '4.5';
                            })()}
                            result="blur"
                        />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                    <radialGradient id="nodeGrad">
                        <stop offset="0%" stopColor="#ffffff" />
                        <stop offset="100%" stopColor={geodeColor} />
                    </radialGradient>
                </defs>

                <g style={{ filter: 'url(#geodeGlow)' }}>
                    {graph.links.map((link) => (
                        <line
                            key={`link-${link.source.id}-${link.target.id}`}
                            x1={link.source.x ?? 0}
                            y1={link.source.y ?? 0}
                            x2={link.target.x ?? 0}
                            y2={link.target.y ?? 0}
                            stroke={geodeColor}
                            strokeOpacity={((): number => {
                                if (isRepairing) return 0.8;
                                if (isHovered) return 0.7;
                                return 0.4;
                            })()}
                            strokeWidth={((): number => {
                                if (isRepairing) return 2;
                                if (isHovered) return 1.5;
                                return 0.8;
                            })()}
                            className="transition-all duration-700"
                            aria-hidden="true"
                        />
                    ))}
                    {graph.nodes.map((node) => (
                        <circle
                            key={node.id}
                            cx={node.x ?? 0}
                            cy={node.y ?? 0}
                            r={((): number => {
                                if (isRepairing) return node.r * 1.5;
                                if (isHovered) return node.r * 1.3;
                                return node.r;
                            })()}
                            fill="url(#nodeGrad)"
                            opacity={isRepairing ? 1 : 0.85 + visualCoherence * 0.15}
                            className={`transition-all duration-500 ease-out outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-black`}
                            role="img" // Keep role img on nodes if meaningful, but they are mostly decorative here.
                            aria-label={`Cognitive Node ${node.id + 1}. Current potential: ${node.r.toFixed(
                                1
                            )} energy units.`}
                        />
                    ))}
                </g>
            </svg>

            {/* Dynamic Background Aura */}
            <div
                className="absolute inset-0 pointer-events-none rounded-full blur-[80px] opacity-15"
                style={{
                    background: `radial-gradient(circle, ${geodeColor} 0%, transparent 80%)`,
                    animation: `aura-pulse ${((): string => {
                        if (isRepairing) return '1s';
                        if (isDreaming) return '12s';
                        return '5s';
                    })()} infinite ease-in-out`,
                }}
                aria-hidden="true"
            />

            <div className="absolute bottom-8 left-1/2 -translate-x-1/2 text-center pointer-events-none w-full px-4">
                <p
                    className={`text-[10px] font-mono uppercase tracking-[0.4em] text-${
                        theme.primary
                    }-400/60 group-hover:text-${theme.primary}-200 transition-all duration-700 ${
                        isRepairing ? 'text-amber-400 animate-pulse' : ''
                    }`}
                >
                    {getStatusText(isRepairing, isDreaming)}
                </p>
                <div
                    className={`mt-2 h-0.5 bg-${theme.primary}-500/10 w-24 mx-auto rounded-full overflow-hidden border border-white/5`}
                >
                    <progress
                        value={Math.round(visualCoherence * 100)}
                        max="100"
                        className={`w-full h-full appearance-none [&::-webkit-progress-bar]:bg-transparent [&::-webkit-progress-value]:bg-${theme.primary}-400 ${
                            isRepairing
                                ? '[&::-webkit-progress-value]:bg-amber-400 [&::-webkit-progress-value]:shadow-[0_0_15px_#fbbf24]'
                                : ''
                        }`}
                        aria-label="System Coherence Index"
                    />
                </div>
            </div>

            <style>{`
        @keyframes aura-pulse {
            0%, 100% { transform: scale(0.85); opacity: 0.1; }
            50% { transform: scale(1.15); opacity: 0.25; }
        }
      `}</style>
        </button>
    );
};

export default PhoenixGeode;
