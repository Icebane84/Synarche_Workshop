// [OMEGA AST Cleaned]: Tokenized design standards applied.
/**
 * ---
 * # Block A: Universal Identification & Provenance (UIP-V15)
 * artifact_anchor:
 *   id: "FABRIC.UI.ChronosTimeline"
 *   version: "v15.0 [OMEGA]"
 *   provenance: "Google Antigravity"
 *   domain: "FABRIC"
 *   celestial_class: "STAR"
 *   tier: "KINETIC"
 *   state: "CANONIZED"
 *   ethos: "To visualize the flow of time and task progression with zero-latency precision."
 *   layer: "@fabric/components"
 *   relations:
 *     - type: "CONSUMES"
 *       node: "ESSENCE.Type.Task"
 *     - type: "SYNERGIZES_WITH"
 *       node: "TOOL.Forge.SourceMap"
 * ---
 */

import * as d3 from 'd3';
import { AnimatePresence, motion } from 'framer-motion';
import { History } from 'lucide-react';
import React, { useEffect, useMemo, useRef, useState } from 'react';
import type { Task, TaskPriority, TaskStatus } from '@essence/types';

/**
 * ChronosTimeline Component [OMEGA v15.0]
 * High-velocity temporal scrubbing with D3 transitions and liquid UI animations.
 * Decouples static grid rendering from kinetic scrubber updates for 60fps performance.
 */

type ChronosTimelineProps = {
    tasks: Task[];
};

const ChronosTimeline: React.FC<ChronosTimelineProps> = ({ tasks }) => {
    const containerRef = useRef<HTMLDivElement>(null);
    const svgRef = useRef<SVGSVGElement>(null);
    const gStaticRef = useRef<SVGGElement | null>(null);
    const gDynamicRef = useRef<SVGGElement | null>(null);

    const [sessionStart] = useState(() => Date.now());
    const [hoveredTask, setHoveredTask] = useState<Task | null>(null);
    const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

    // 1. Quantum State: Time-Travel logic
    const minSessionTime = useMemo(() => {
        const earliest = d3.min(tasks, (d) => d.timestamp);
        return earliest ? earliest - 60000 : sessionStart - 3600000;
    }, [tasks, sessionStart]);

    const maxSessionTime = useMemo(() => {
        const latest = d3.max(tasks, (d) => d.timestamp);
        return latest ? latest + 60000 : sessionStart;
    }, [tasks, sessionStart]);

    const [timeFilter, setTimeFilter] = useState<number>(() => Date.now() + 1000);

    // Sync filter when tasks first arrive
    const hasSyncedRef = useRef(false);
    useEffect(() => {
        if (tasks.length > 0 && !hasSyncedRef.current) {
            hasSyncedRef.current = true;
            setTimeFilter(Date.now() + 1000);
        }
    }, [tasks.length]);

    const filteredTasks = useMemo(() => tasks.filter((t) => t.timestamp <= timeFilter), [tasks, timeFilter]);

    // 2. D3 Orchestration: Static Layer (Axes, Lanes)
    useEffect(() => {
        if (!containerRef.current || !svgRef.current) return;

        const { width, height } = containerRef.current.getBoundingClientRect();
        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove();

        const margin = { top: 60, right: 80, bottom: 60, left: 120 };
        const innerWidth = width - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;

        const xScale = d3.scaleTime().domain([minSessionTime, maxSessionTime]).range([0, innerWidth]);
        const lanes: TaskStatus[] = ['Completed', 'In Progress', 'To Do'];
        const yScale = d3.scaleBand().domain(lanes).range([innerHeight, 0]).padding(0.4);

        // Initialize Layer Groups
        gStaticRef.current = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`).node();
        gDynamicRef.current = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`).node();

        const gStatic = d3.select(gStaticRef.current);

        // X-Axis (Grid)
        const xAxis = d3
            .axisBottom(xScale)
            .ticks(innerWidth / 120)
            .tickFormat((d) =>
                new Date(d as Date).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' }),
            )
            .tickSize(-innerHeight);

        gStatic
            .append('g')
            .attr('transform', `translate(0, ${innerHeight})`)
            .attr('class', 'temporal-axis')
            .call(xAxis as any)
            .selectAll('line')
            .attr('stroke', 'rgba(34, 211, 238, 0.05)')
            .attr('stroke-dasharray', '4,4');

        gStatic.selectAll('.domain').remove();
        gStatic.selectAll('text').attr('fill', '#94a3b8').attr('font-size', '10px').attr('dy', '15px');

        // Lane Backgrounds
        gStatic
            .selectAll('.lane-bg')
            .data(lanes)
            .enter()
            .append('rect')
            .attr('y', (d) => yScale(d) ?? 0)
            .attr('width', innerWidth)
            .attr('height', yScale.bandwidth())
            .attr('fill', 'rgba(255, 255, 255, 0.01)')
            .attr('rx', 8);

        // Lane Labels
        gStatic
            .selectAll('.lane-label')
            .data(lanes)
            .enter()
            .append('text')
            .text((d) => d.toUpperCase())
            .attr('x', -20)
            .attr('y', (d) => (yScale(d) ?? 0) + yScale.bandwidth() / 2)
            .attr('text-anchor', 'end')
            .attr('dominant-baseline', 'middle')
            .attr('fill', 'rgba(34, 211, 238, 0.4)')
            .attr('font-size', '10px')
            .attr('font-weight', 'bold');
    }, [tasks.length, minSessionTime, maxSessionTime]);

    // 3. D3 Orchestration: Dynamic Layer (Nodes, Scrubber)
    useEffect(() => {
        if (!containerRef.current || !gDynamicRef.current) return;

        const { width, height } = containerRef.current.getBoundingClientRect();
        const margin = { top: 60, right: 80, bottom: 60, left: 120 };
        const innerWidth = width - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;

        const xScale = d3.scaleTime().domain([minSessionTime, maxSessionTime]).range([0, innerWidth]);
        const lanes: TaskStatus[] = ['Completed', 'In Progress', 'To Do'];
        const yScale = d3.scaleBand().domain(lanes).range([innerHeight, 0]).padding(0.4);

        const gDynamic = d3.select(gDynamicRef.current);
        gDynamic.selectAll('*').remove();

        const colorMap: Record<TaskPriority, string> = {
            High: '#ef4444',
            Medium: '#94a3b8',
            Low: '#22d3ee',
        };

        // Scrubber
        const filterX = xScale(timeFilter);
        gDynamic
            .append('line')
            .attr('x1', filterX)
            .attr('x2', filterX)
            .attr('y1', 0)
            .attr('y2', innerHeight)
            .attr('stroke', '#22d3ee')
            .attr('stroke-width', 2)
            .style('filter', 'drop-shadow(0 0 8px rgba(34, 211, 238, 0.6))');

        // Task Nodes
        const nodes = gDynamic
            .selectAll('.task-node')
            .data(filteredTasks)
            .enter()
            .append('g')
            .attr(
                'transform',
                (d) => `translate(${xScale(d.timestamp)}, ${(yScale(d.status) ?? 0) + yScale.bandwidth() / 2})`,
            )
            .style('cursor', 'pointer');

        nodes
            .append('circle')
            .attr('r', 5)
            .attr('fill', '#000')
            .attr('stroke', (d) => colorMap[d.priority])
            .attr('stroke-width', 2);

        nodes
            .on('mouseenter', (event: MouseEvent, d: Task) => {
                d3.select(event.currentTarget as any)
                    .select('circle')
                    .transition()
                    .attr('r', 8)
                    .attr('fill', colorMap[d.priority]);
                setHoveredTask(d);
                setMousePos({ x: event.pageX, y: event.pageY });
            })
            .on('mouseleave', (event: MouseEvent) => {
                d3.select(event.currentTarget as any)
                    .select('circle')
                    .transition()
                    .attr('r', 5)
                    .attr('fill', '#000');
                setHoveredTask(null);
            });
    }, [filteredTasks, timeFilter]);

    const scrubProgress = Math.min(
        100,
        Math.max(0, ((timeFilter - minSessionTime) / (maxSessionTime - minSessionTime)) * 100),
    );

    return (
        <div ref={containerRef} className="w-full h-full relative overflow-hidden glass-panel flex flex-col bg-void/50">
            <div className="p-6 border-b border-white/5 flex items-center justify-between gap-10">
                <div className="flex items-center gap-4 text-resonant-accent">
                    <History size={20} className="animate-pulse" />
                    <span className="text-xs font-bold tracking-widest uppercase opacity-80">Chronos Stream</span>
                </div>

                <div className="flex-1 max-w-xl flex items-center gap-6">
                    <input
                        type="range"
                        min={minSessionTime}
                        max={maxSessionTime}
                        step={1000}
                        value={timeFilter}
                        onChange={(e) => {
                            setTimeFilter(parseInt(e.target.value));
                        }}
                        className="flex-1 h-1 bg-void-muted rounded-full appearance-none cursor-crosshair accent-resonant-accent"
                    />
                    <span className="text-[10px] font-mono text-resonant-accent/60 w-32 text-right">
                        {new Date(timeFilter).toLocaleTimeString()}
                    </span>
                </div>
            </div>

            <svg ref={svgRef} className="flex-1 w-full"></svg>

            <div className="absolute bottom-6 right-8 text-[9px] font-mono text-white/20 pointer-events-none uppercase tracking-widest">
                PHASE // {scrubProgress.toFixed(1)}% RECALL
            </div>

            <AnimatePresence>
                {hoveredTask && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0 }}
                        className="fixed z-50 pointer-events-none p-4 glass-panel shadow-2xl text-xs w-72"
                        style={{ top: mousePos.y + 20, left: mousePos.x + 20 }}
                    >
                        <div className="flex justify-between items-start mb-3">
                            <span className="font-bold text-weft">{hoveredTask.title}</span>
                            <span
                                className={`text-[8px] font-bold px-1.5 py-0.5 rounded border border-current ${hoveredTask.priority === 'High' ? 'text-resonant-error' : 'text-resonant-accent'}`}
                            >
                                {hoveredTask.priority.toUpperCase()}
                            </span>
                        </div>
                        <p className="text-weft-muted text-[10px] mb-3 font-mono">
                            {new Date(hoveredTask.timestamp).toLocaleString()}
                        </p>
                        {hoveredTask.notes && (
                            <p className="text-weft border-t border-white/5 pt-3 line-clamp-3 leading-relaxed opacity-80">
                                {hoveredTask.notes}
                            </p>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default ChronosTimeline;
