import * as d3 from 'd3';
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useSignal } from '../hooks/useSignal';
import { useTheme } from '../hooks/useTheme';
import { SignalType } from '@system/signalBus';
import { EnhancedCoherenceState, useCoherenceStore } from '../store/coherenceStore';
import { useUIStore } from '../store/uiStore';

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

interface ProcessedLink extends d3.SimulationLinkDatum<Node> {
    source: Node;
    target: Node;
}

const getRandomFloat = (): number => {
    const array = new Uint32Array(1);
    crypto.getRandomValues(array);
    return array[0] / (0xffffffff + 1);
};

const PhoenixGeode: React.FC = () => {
    const containerRef = useRef<HTMLDivElement>(null);
    const simulationRef = useRef<d3.Simulation<Node, ProcessedLink> | null>(null);
    const [graph, setGraph] = useState<{ nodes: Node[]; links: ProcessedLink[] }>({ nodes: [], links: [] });
    const [isHovered, setIsHovered] = useState(false);
    const [size, setSize] = useState({ width: 0, height: 0 });

    const coherenceIndex = useCoherenceStore((state) => state.coherenceIndex);
    const isDreaming = useCoherenceStore((state) => state.isDreaming);
    // Enhanced store access for isRepairing
    const isRepairing = useCoherenceStore((state: EnhancedCoherenceState) => state.isRepairing);
    const openSynapse = useUIStore((state) => state.openSynapse);
    const theme = useTheme();
    const [isRippling, setIsRippling] = useState(false);

    // --- [RESONANCE LISTENER] ---
    useSignal(SignalType.COHERENCE_RIPPLE, (data) => {
        if (!data.meta?.isGlobal) return;
        setIsRippling(true);

        // Inject kinetic energy into the D3 simulation
        if (simulationRef.current) {
            simulationRef.current.alphaTarget(0.8).restart();
        }

        // Decay the ripple
        setTimeout(() => {
            setIsRippling(false);
            if (simulationRef.current) {
                simulationRef.current.alphaTarget(0.3);
            }
        }, 400);
    });
    // ----------------------------

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
        const animate = () => {
            setVisualCoherence((prev) => {
                const diff = targetCoherenceRef.current - prev;
                if (Math.abs(diff) < 0.001) return targetCoherenceRef.current;
                return prev + diff * 0.05; // 5% interpolation per frame for smoothness
            });
            animationFrameId = requestAnimationFrame(animate);
        };
        animate();
        return () => {
            cancelAnimationFrame(animationFrameId);
        };
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
            r: (isRepairing ? 4 : 2.5) + getRandomFloat() * 5,
            color: geodeColor,
        }));

        const links: ProcessedLink[] = d3.range(numNodes).map((i) => ({
            source: nodes[Math.floor(Math.sqrt(i))],
            target: nodes[i],
        }));

        const simulation = d3
            .forceSimulation<Node>(nodes)
            .velocityDecay(0.4) // High friction for stable, fluid movement
            .force(
                'link',
                d3
                    .forceLink<Node, ProcessedLink>(links)
                    .id((d) => d.id)
                    .distance(isRepairing ? 15 : 25)
                    .strength(isRepairing ? 0.8 : 0.3),
            )
            .force('charge', d3.forceManyBody().strength(isRepairing ? -200 : -100))
            .force('center', d3.forceCenter(width / 2, height / 2).strength(0.6)) // Aggressive centering forces (FIX: PREVENT DRIFT)
            .force(
                'collide',
                d3
                    .forceCollide<Node>()
                    .radius((d) => d.r + (isRepairing ? 5 : 8))
                    .strength(0.5),
            )
            .force('x', d3.forceX(width / 2).strength(isRepairing ? 0.2 : 0.1)) // Stronger X-axis containment
            .force('y', d3.forceY(height / 2).strength(isRepairing ? 0.2 : 0.1)); // Stronger Y-axis containment

        simulation.on('tick', () => {
            const linkForce = simulation.force('link') as d3.ForceLink<Node, ProcessedLink>;
            if (linkForce) {
                setGraph({
                    nodes: [...simulation.nodes()],
                    links: linkForce.links(),
                });
            }
        });

        simulationRef.current = simulation;
        return () => {
            simulation.stop();
        };
    }, [size.width, size.height, geodeColor, isRepairing]);

    useEffect(() => {
        if (simulationRef.current) {
            const forceStrength = isRepairing ? -300 : isHovered ? -150 : -100 + visualCoherence * 30;
            const chargeForce = simulationRef.current.force('charge') as d3.ForceManyBody<Node>;
            if (chargeForce) {
                chargeForce.strength(forceStrength);
            }

            // Perpetual low-energy reheat for constant fluid drift
            simulationRef.current.alphaTarget(0.3).restart();
        }
    }, [isHovered, visualCoherence, isRepairing]);

    useEffect(() => {
        const handleResize = () => {
            if (containerRef.current) {
                const { width, height } = containerRef.current.getBoundingClientRect();
                setSize({ width, height });
                if (simulationRef.current) {
                    simulationRef.current.force('center', d3.forceCenter(width / 2, height / 2).strength(0.6));
                    simulationRef.current.force('x', d3.forceX(width / 2).strength(0.1));
                    simulationRef.current.force('y', d3.forceY(height / 2).strength(0.1));
                    simulationRef.current.alpha(0.3).restart();
                }
            }
        };
        window.addEventListener('resize', handleResize);
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            openSynapse();
        }
    };

    return (
        <div
            ref={containerRef}
            className={`w-full h-full relative cursor-pointer group transition-all duration-1000 ease-out transform outline-none rounded-lg focus-visible:ring-2 focus-visible:ring-${
                theme.primary
            }-400/50 ${isHovered ? 'scale-[1.04]' : 'scale-100'}`}
            style={{ contain: 'content' }}
            onMouseEnter={() => {
                setIsHovered(true);
            }}
            onMouseLeave={() => {
                setIsHovered(false);
            }}
            onClick={openSynapse}
            onKeyDown={handleKeyDown}
            role="button"
            tabIndex={0}
            aria-label={`Phoenix Geode: A real-time visualization of cognitive coherence. Current index: ${Math.round(
                coherenceIndex * 100,
            ).toString()} percent. ${
                isRepairing
                    ? 'Repair sequence is active.'
                    : isDreaming
                      ? 'System is in background dreaming mode.'
                      : 'Neural substrate is synchronized.'
            } Press Enter to open the Synapse.`}
        >
            <svg className="w-full h-full overflow-visible" role="presentation">
                <defs>
                    <filter id="geodeGlow" x="-100%" y="-100%" width="300%" height="300%">
                        <feGaussianBlur
                            stdDeviation={isRepairing ? '12' : isRippling ? '25' : isHovered ? '8' : '4.5'}
                            result="blur"
                        />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                        {isRippling && (
                            <feColorMatrix
                                type="matrix"
                                values="1.2 0 0 0 0  0 1.2 0 0 0  0 0 1.2 0 0  0 0 0 1 0"
                                result="bright"
                            />
                        )}
                    </filter>
                    <radialGradient id="nodeGrad">
                        <stop offset="0%" stopColor="#ffffff" />
                        <stop offset="100%" stopColor={geodeColor} />
                    </radialGradient>
                </defs>

                <g style={{ filter: 'url(#geodeGlow)' }}>
                    {graph.links.map((link, i) => (
                        <line
                            key={`link-${i}`}
                            x1={link.source.x}
                            y1={link.source.y}
                            x2={link.target.x}
                            y2={link.target.y}
                            stroke={geodeColor}
                            strokeOpacity={isRepairing ? 0.8 : isHovered ? 0.7 : 0.4}
                            strokeWidth={isRepairing ? 2 : isHovered ? 1.5 : 0.8}
                            className="transition-all duration-700"
                            aria-hidden="true"
                        />
                    ))}
                    {graph.nodes.map((node) => (
                        <circle
                            key={node.id}
                            r={
                                isRepairing
                                    ? node.r * 1.5
                                    : isRippling
                                      ? node.r * 2.2
                                      : isHovered
                                        ? node.r * 1.3
                                        : node.r
                            }
                            fill="url(#nodeGrad)"
                            opacity={isRepairing || isRippling ? 1.0 : 0.85 + visualCoherence * 0.15}
                            style={{ 
                                transform: `translate(${(node.x ?? 0).toString()}px, ${(node.y ?? 0).toString()}px)`,
                                willChange: 'transform'
                            }}
                            className={`transition-all duration-300 ease-out outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-black`}
                            role="img"
                            tabIndex={-1}
                            aria-label={`Cognitive Node ${node.id.toString()}. Current potential: ${node.r.toFixed(
                                1,
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
                    animation: `aura-pulse ${isRepairing ? '1s' : isDreaming ? '12s' : '5s'} infinite ease-in-out`,
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
                    {isRepairing
                        ? '[REPAIR SEQUENCE ACTIVE]'
                        : isDreaming
                          ? '[COGNITIVE REM PHASE]'
                          : 'Neural Substrate Synchronized'}
                </p>
                <div
                    className={`mt-2 h-0.5 bg-${theme.primary}-500/10 w-24 mx-auto rounded-full overflow-hidden border border-white/5`}
                >
                    <div
                        className={`h-full ${
                            isRepairing ? 'bg-amber-400 shadow-[0_0_15px_#fbbf24]' : `bg-${theme.primary}-400`
                        } transition-all duration-1000 ease-in-out`}
                        style={{ width: `${(visualCoherence * 100).toString()}%` }}
                        role="progressbar"
                        aria-valuenow={Math.round(visualCoherence * 100)}
                        aria-valuemin={0}
                        aria-valuemax={100}
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
        </div>
    );
};

export default PhoenixGeode;
