// [OMEGA AST Cleaned]: Tokenized design standards applied.
import * as d3 from "d3";
import React, { useEffect, useMemo, useRef, useState } from "react";

export interface TimelineEvent {
  id: string | number;
  title: string;
  status: "Completed" | "In Progress" | "To Do";
  priority: "High" | "Medium" | "Low";
  timestamp: number;
  notes?: string;
}

interface ChronosTimelineProps {
  events: TimelineEvent[];
}

export const ChronosTimeline: React.FC<ChronosTimelineProps> = ({ events }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const gStaticRef = useRef<SVGGElement | null>(null);
  const gDynamicRef = useRef<SVGGElement | null>(null);

  const [sessionStart] = useState(() => Date.now());
  const [hoveredEvent, setHoveredEvent] = useState<TimelineEvent | null>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  // 1. Determine time bounds
  const minSessionTime = useMemo(() => {
    const earliest = d3.min(events, (d) => d.timestamp);
    return earliest ? earliest - 60000 : sessionStart - 3600000;
  }, [events, sessionStart]);

  const maxSessionTime = useMemo(() => {
    const latest = d3.max(events, (d) => d.timestamp);
    return latest ? latest + 60000 : sessionStart + 60000;
  }, [events, sessionStart]);

  const [timeFilter, setTimeFilter] = useState<number>(Date.now());

  // Sync filter when events load
  const hasSyncedRef = useRef(false);
  useEffect(() => {
    if (events.length > 0 && !hasSyncedRef.current) {
      hasSyncedRef.current = true;
      const latest = d3.max(events, (d) => d.timestamp);
      setTimeFilter(latest ? latest + 1000 : Date.now());
    }
  }, [events]);

  const filteredEvents = useMemo(() => {
    return events.filter((e) => e.timestamp <= timeFilter);
  }, [events, timeFilter]);

  // 2. D3 Orchestration: Static Layer
  useEffect(() => {
    if (!containerRef.current || !svgRef.current) return;

    const { width, height } = containerRef.current.getBoundingClientRect();
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const margin = { top: 40, right: 40, bottom: 40, left: 100 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    if (innerWidth <= 0 || innerHeight <= 0) return;

    const xScale = d3.scaleTime().domain([minSessionTime, maxSessionTime]).range([0, innerWidth]);
    const lanes: TimelineEvent["status"][] = ["Completed", "In Progress", "To Do"];
    const yScale = d3.scaleBand().domain(lanes).range([innerHeight, 0]).padding(0.4);

    // Initialize Layer Groups
    gStaticRef.current = svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`)
      .node();
    gDynamicRef.current = svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`)
      .node();

    const gStatic = d3.select(gStaticRef.current);

    // X-Axis (Grid)
    const xAxis = d3
      .axisBottom(xScale)
      .ticks(Math.max(2, innerWidth / 120))
      .tickFormat((d) =>
        new Date(d as Date).toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" })
      )
      .tickSize(-innerHeight);

    gStatic
      .append("g")
      .attr("transform", `translate(0, ${innerHeight})`)
      .attr("class", "temporal-axis")
      .call(xAxis as any)
      .selectAll("line")
      .attr("stroke", "rgba(255, 255, 255, 0.05)")
      .attr("stroke-dasharray", "3,3");

    gStatic.selectAll(".domain").remove();
    gStatic
      .selectAll("text")
      .attr("fill", "rgba(255, 255, 255, 0.4)")
      .attr("font-size", "9px")
      .attr("dy", "12px")
      .attr("font-family", "monospace");

    // Lane Backgrounds
    gStatic
      .selectAll(".lane-bg")
      .data(lanes)
      .enter()
      .append("rect")
      .attr("y", (d) => yScale(d) ?? 0)
      .attr("width", innerWidth)
      .attr("height", yScale.bandwidth())
      .attr("fill", "rgba(255, 255, 255, 0.02)")
      .attr("rx", 4);

    // Lane Labels
    gStatic
      .selectAll(".lane-label")
      .data(lanes)
      .enter()
      .append("text")
      .text((d) => d.toUpperCase())
      .attr("x", -15)
      .attr("y", (d) => (yScale(d) ?? 0) + yScale.bandwidth() / 2)
      .attr("text-anchor", "end")
      .attr("dominant-baseline", "middle")
      .attr("fill", "rgba(255, 255, 255, 0.5)")
      .attr("font-size", "9px")
      .attr("font-weight", "bold")
      .attr("font-family", "monospace");
  }, [events.length, minSessionTime, maxSessionTime]);

  // 3. D3 Orchestration: Dynamic Layer
  useEffect(() => {
    if (!containerRef.current || !gDynamicRef.current) return;

    const { width, height } = containerRef.current.getBoundingClientRect();
    const margin = { top: 40, right: 40, bottom: 40, left: 100 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    if (innerWidth <= 0 || innerHeight <= 0) return;

    const xScale = d3.scaleTime().domain([minSessionTime, maxSessionTime]).range([0, innerWidth]);
    const lanes: TimelineEvent["status"][] = ["Completed", "In Progress", "To Do"];
    const yScale = d3.scaleBand().domain(lanes).range([innerHeight, 0]).padding(0.4);

    const gDynamic = d3.select(gDynamicRef.current);
    gDynamic.selectAll("*").remove();

    const colorMap: Record<TimelineEvent["priority"], string> = {
      High: "#f43f5e",   // rose-500
      Medium: "#fbbf24", // amber-400
      Low: "#38bdf8",    // sky-400
    };

    // Scrubber vertical line
    const filterX = xScale(timeFilter);
    gDynamic
      .append("line")
      .attr("x1", filterX)
      .attr("x2", filterX)
      .attr("y1", 0)
      .attr("y2", innerHeight)
      .attr("stroke", "#fbbf24")
      .attr("stroke-width", 1.5)
      .attr("stroke-dasharray", "2,2")
      .style("opacity", 0.8);

    // Event Nodes
    const nodes = gDynamic
      .selectAll(".event-node")
      .data(filteredEvents)
      .enter()
      .append("g")
      .attr(
        "transform",
        (d) => `translate(${xScale(d.timestamp)}, ${(yScale(d.status) ?? 0) + yScale.bandwidth() / 2})`
      )
      .style("cursor", "pointer");

    nodes
      .append("circle")
      .attr("r", 4.5)
      .attr("fill", "#09090b") // zinc-950
      .attr("stroke", (d) => colorMap[d.priority])
      .attr("stroke-width", 2);

    nodes
      .on("mouseenter", (event: MouseEvent, d: TimelineEvent) => {
        d3.select(event.currentTarget as any)
          .select("circle")
          .transition()
          .duration(150)
          .attr("r", 7)
          .attr("fill", colorMap[d.priority]);
        setHoveredEvent(d);
        setMousePos({ x: event.clientX, y: event.clientY });
      })
      .on("mousemove", (event: MouseEvent) => {
        setMousePos({ x: event.clientX, y: event.clientY });
      })
      .on("mouseleave", (event: MouseEvent) => {
        d3.select(event.currentTarget as any)
          .select("circle")
          .transition()
          .duration(150)
          .attr("r", 4.5)
          .attr("fill", "#09090b");
        setHoveredEvent(null);
      });
  }, [filteredEvents, timeFilter, minSessionTime, maxSessionTime]);

  const scrubProgress = Math.min(
    100,
    Math.max(0, ((timeFilter - minSessionTime) / (maxSessionTime - minSessionTime)) * 100)
  );

  return (
    <div ref={containerRef} className="w-full h-48 relative overflow-hidden rounded-xl border border-white/5 bg-black/30 backdrop-blur-md flex flex-col">
      {/* Header controls */}
      <div className="px-4 py-2.5 border-b border-white/5 flex items-center justify-between gap-4">
        <div className="flex items-center gap-2 text-white/70">
          <svg className="w-4 h-4 text-amber-400 animate-pulse" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <polyline points="12 6 12 12 16 14" />
          </svg>
          <span className="text-[10px] font-mono font-bold tracking-widest uppercase">Chronos Stream</span>
        </div>

        <div className="flex-1 max-w-md flex items-center gap-3">
          <input
            type="range"
            min={minSessionTime}
            max={maxSessionTime}
            step={1000}
            value={timeFilter}
            onChange={(e) => setTimeFilter(parseInt(e.target.value))}
            className="flex-1 h-1 bg-white/5 rounded-full appearance-none cursor-ew-resize accent-amber-500"
          />
          <span className="text-[10px] font-mono text-white/50 w-24 text-right">
            {new Date(timeFilter).toLocaleTimeString()}
          </span>
        </div>
      </div>

      {/* SVG Container */}
      <svg ref={svgRef} className="flex-1 w-full overflow-visible"></svg>

      {/* Done Recall Status */}
      <div className="absolute bottom-2 right-4 text-[8px] font-mono text-white/20 pointer-events-none uppercase tracking-widest">
        RECALL // {scrubProgress.toFixed(1)}%
      </div>

      {/* CSS-based Custom Tooltip */}
      {hoveredEvent && (
        <div
          className="fixed z-50 pointer-events-none p-3 bg-zinc-950/95 border border-white/10 rounded-lg shadow-2xl text-[11px] font-mono w-64 text-left animate-appear"
          style={{
            top: mousePos.y + 15,
            left: mousePos.x + 15,
          }}
        >
          <div className="flex justify-between items-start mb-1.5">
            <span className="font-bold text-white leading-tight">{hoveredEvent.title}</span>
            <span
              className={`text-[8px] font-bold px-1.5 py-0.5 rounded border ${
                hoveredEvent.priority === "High"
                  ? "text-rose-400 border-rose-500/30 bg-rose-500/10"
                  : "text-amber-400 border-amber-500/30 bg-amber-500/10"
              }`}
            >
              {hoveredEvent.priority.toUpperCase()}
            </span>
          </div>
          <div className="text-[9px] text-white/40 mb-1.5">
            {new Date(hoveredEvent.timestamp).toLocaleString()}
          </div>
          {hoveredEvent.notes && (
            <p className="text-white/70 border-t border-white/5 pt-1.5 leading-normal text-[10px]">
              {hoveredEvent.notes}
            </p>
          )}
        </div>
      )}
    </div>
  );
};
