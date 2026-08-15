import { useState } from "react";

// ==========================================
// CANONICAL SEVEN-SOVEREIGN METADATA (PPL)
// ==========================================
export interface SovereignTier {
  id: string;
  name: string;
  x: number;
  y: number;
  radius: number;
  color: string;
  glow: string;
  desc: string;
}

export interface SynergisticLink {
  source: string;
  target: string;
  type: string;
}

export interface DissonanceQuest {
  id: string;
  title: string;
  target: string;
  status: string;
  severity: string;
}

const SOVEREIGN_TIERS: SovereignTier[] = [
  {
    id: "GVRN",
    name: "0_GOVERNANCE",
    x: 400,
    y: 80,
    radius: 35,
    color: "#ff3366",
    glow: "rgba(255, 51, 102, 0.6)",
    desc: "Seat of system law: Codex, UEBs, and Primary Laws.",
  },
  {
    id: "UMB",
    name: "1_BLUEPRINTS",
    x: 220,
    y: 180,
    radius: 28,
    color: "#00f0ff",
    glow: "rgba(0, 240, 255, 0.5)",
    desc: 'Structural definitions and Module Blueprints (The "What").',
  },
  {
    id: "AOP",
    name: "2_PROTOCOLS",
    x: 580,
    y: 180,
    radius: 28,
    color: "#33ff66",
    glow: "rgba(51, 255, 102, 0.5)",
    desc: 'Operational Playbooks and Execution Standards (The "How").',
  },
  {
    id: "GUCA",
    name: "3_COMMANDS",
    x: 180,
    y: 380,
    radius: 26,
    color: "#ffff33",
    glow: "rgba(255, 255, 51, 0.5)",
    desc: "Executable Command Architecture and Prompt Templates.",
  },
  {
    id: "SELT",
    name: "4_LOGS",
    x: 620,
    y: 380,
    radius: 26,
    color: "#ff9933",
    glow: "rgba(255, 153, 51, 0.5)",
    desc: 'Historical repository for Experience Logs (The "Result").',
  },
  {
    id: "AXION",
    name: "5_IDENTITY",
    x: 400,
    y: 450,
    radius: 30,
    color: "#cc33ff",
    glow: "rgba(204, 51, 255, 0.6)",
    desc: "Identity Manifests, Persona Files, and core self-definitions.",
  },
  {
    id: "CORE",
    name: "6_ASSETS",
    x: 400,
    y: 270,
    radius: 45,
    color: "#ffffff",
    glow: "rgba(255, 255, 255, 0.7)",
    desc: "The Phoenix Engine Core, underlying scripts, and system tools.",
  },
];

const SYNERGISTIC_LINKS: SynergisticLink[] = [
  { source: "GVRN", target: "CORE", type: "GOVERNS" },
  { source: "UMB", target: "CORE", type: "DEFINES" },
  { source: "AOP", target: "CORE", type: "OPERATES" },
  { source: "GUCA", target: "AOP", type: "TRIGGERS" },
  { source: "CORE", target: "SELT", type: "TELEMETRY" },
  { source: "AXION", target: "GVRN", type: "ALIGNS" },
  { source: "UMB", target: "AOP", type: "STRUCTURATES" },
];

export function NetworkGraph(): React.JSX.Element {
  const [selectedNode, setSelectedNode] = useState<SovereignTier>(SOVEREIGN_TIERS[6]); // Defaults to Engine Core
  const [cyclePhase, setCyclePhase] = useState<
    "COHERENCE" | "DISSONANCE" | "SYNTHESIS" | "TRANSCENDENCE"
  >("COHERENCE");
  const [dissonanceQuests] = useState<DissonanceQuest[]>([
    {
      id: "DQ-001",
      title: "Eradicate Relative Path Space Junk",
      target: "6_ASSETS",
      status: "ACTIVE",
      severity: "HIGH",
    },
    {
      id: "DQ-002",
      title: "Resolve Form 1095-A Tax Discrepancy",
      target: "0_GOVERNANCE",
      status: "ACTIVE",
      severity: "CRITICAL",
    },
  ]);

  // Handle visual pacing of the Phoenix Cycle transmutation logic
  const triggerPhoenixCycle = (): void => {
    setCyclePhase("DISSONANCE");
    setTimeout(() => {
      setCyclePhase("SYNTHESIS");
      setTimeout(() => {
        setCyclePhase("TRANSCENDENCE");
        setTimeout(() => {
          setCyclePhase("COHERENCE");
        }, 2500);
      }, 2500);
    }, 2000);
  };

  const getStatusColor = (): string => {
    if (cyclePhase === "COHERENCE") return "#064e3b";
    if (cyclePhase === "DISSONANCE") return "#7f1d1d";
    return "#7c2d12";
  };

  return (
    <div
      style={{
        backgroundColor: "#00001a",
        color: "#cbd5e1",
        padding: "24px",
        borderRadius: "12px",
        fontFamily: "sans-serif",
        maxWidth: "1000px",
        margin: "0 auto",
        border: "1px solid #1e1e38",
      }}
    >
      {/* Visual Header / Control Panel */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          borderBottom: "1px solid #1e1e38",
          paddingBottom: "16px",
          marginBottom: "20px",
        }}
      >
        <div>
          <h2 style={{ color: "#ffffff", fontSize: "24px", fontWeight: "bold", margin: 0 }}>
            Phoenix Core Engine Workspace
          </h2>
          <p style={{ color: "#64748b", fontSize: "14px", marginTop: "4px" }}>
            Autonomous Knowledge Mesh Navigation Portal
          </p>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", gap: "12px", alignItems: "center" }}>
          <div
            style={{
              padding: "6px 12px",
              borderRadius: "6px",
              fontSize: "12px",
              fontWeight: "bold",
              backgroundColor: getStatusColor(),
              color: "#ffffff",
            }}
          >
            SYSTEM STATUS: {cyclePhase}
          </div>
          <button
            type="button"
            onClick={triggerPhoenixCycle}
            disabled={cyclePhase !== "COHERENCE"}
            style={{
              padding: "8px 16px",
              backgroundColor: "#0d9488",
              color: "#ffffff",
              border: "none",
              borderRadius: "6px",
              cursor: cyclePhase === "COHERENCE" ? "pointer" : "not-allowed",
              fontWeight: "600",
              opacity: cyclePhase === "COHERENCE" ? 1 : 0.5,
            }}
          >
            Forge Ultimate Synergy
          </button>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: "24px" }}>
        {cyclePhase === "COHERENCE" && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
            {/* Visual Canvas Panel */}
            <div
              style={{
                backgroundColor: "#000026",
                borderRadius: "8px",
                padding: "16px",
                border: "1px solid #1e1e38",
                position: "relative",
              }}
            >
              <h4
                style={{
                  color: "#94a3b8",
                  fontSize: "14px",
                  fontWeight: "600",
                  marginBottom: "12px",
                }}
              >
                Interactive Topological Network
              </h4>
              <svg width="100%" height="500" viewBox="0 0 800 550" style={{ overflow: "visible" }}>
                <title>Topological Network Graph</title>
                <defs>
                  {/* Glowing configurations per blueprint spec */}
                  {SOVEREIGN_TIERS.map((tier) => (
                    <filter
                      id={`glow-${tier.id}`}
                      key={tier.id}
                      x="-50%"
                      y="-50%"
                      width="200%"
                      height="200%"
                    >
                      <feGaussianBlur stdDeviation="8" result="coloredBlur" />
                      <feMerge>
                        <feMergeNode in="coloredBlur" />
                        <feMergeNode in="SourceGraphic" />
                      </feMerge>
                    </filter>
                  ))}
                </defs>

                {/* Draw Synergy Links */}
                {SYNERGISTIC_LINKS.map((link) => {
                  const sNode = SOVEREIGN_TIERS.find((n) => n.id === link.source);
                  const tNode = SOVEREIGN_TIERS.find((n) => n.id === link.target);
                  if (!sNode || !tNode) return null;
                  const pathKey = `${link.source}-${link.target}`;
                  return (
                    <g key={pathKey}>
                      <line
                        x1={sNode.x}
                        y1={sNode.y}
                        x2={tNode.x}
                        y2={tNode.y}
                        style={{ stroke: "#1e293b", strokeWidth: 2 }}
                      />
                      <circle r="3" fill="#0d9488">
                        <animateMotion
                          dur="4s"
                          repeatCount="indefinite"
                          path={`M ${sNode.x} ${sNode.y} L ${tNode.x} ${tNode.y}`}
                        />
                      </circle>
                    </g>
                  );
                })}

                {/* Draw Sovereign Nodes */}
                {SOVEREIGN_TIERS.map((tier) => {
                  const isSelected = selectedNode.id === tier.id;
                  const hasQuest = dissonanceQuests.some((q) => q.target === tier.name);
                  return (
                    // biome-ignore lint/a11y/useSemanticElements: SVG elements are not semantic buttons
                    <g
                      key={tier.id}
                      transform={`translate(${tier.x}, ${tier.y})`}
                      onClick={() => setSelectedNode(tier)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter" || e.key === " ") {
                          setSelectedNode(tier);
                        }
                      }}
                      role="button"
                      tabIndex={0}
                      style={{ cursor: "pointer" }}
                    >
                      {/* Active Pulse Area */}
                      <circle
                        r={tier.radius + (isSelected ? 6 : 0)}
                        fill="transparent"
                        stroke={hasQuest ? "#ef4444" : tier.color}
                        strokeWidth={isSelected ? 3 : 1.5}
                        filter={`url(#glow-${tier.id})`}
                        style={{ opacity: isSelected ? 0.9 : 0.4 }}
                      />
                      <circle r={tier.radius} fill="#000033" stroke={tier.color} strokeWidth={2} />
                      {/* Operational Center Core Indicator */}
                      {hasQuest && (
                        <circle r={tier.radius} fill="none" stroke="#ef4444" strokeWidth={2}>
                          <animate
                            attributeName="r"
                            values={`${tier.radius};${tier.radius + 8};${tier.radius}`}
                            dur="2s"
                            repeatCount="indefinite"
                          />
                          <animate
                            attributeName="opacity"
                            values="1;0;1"
                            dur="2s"
                            repeatCount="indefinite"
                          />
                        </circle>
                      )}
                      <text
                        textAnchor="middle"
                        dy=".3em"
                        fill="#ffffff"
                        style={{
                          fontSize: "11px",
                          fontWeight: "bold",
                          fontFamily: "monospace",
                          letterSpacing: "0.5px",
                        }}
                      >
                        {tier.id}
                      </text>
                    </g>
                  );
                })}
              </svg>
            </div>

            {/* Context Inspection Panels */}
            <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
              {/* Selected Tier Inspector */}
              <div
                style={{
                  backgroundColor: "#07071f",
                  borderLeft: `4px solid ${selectedNode.color}`,
                  padding: "16px",
                  borderRadius: "6px",
                }}
              >
                <span
                  style={{ fontSize: "12px", fontFamily: "monospace", color: selectedNode.color }}
                >
                  {selectedNode.id} REGISTRY LOCK
                </span>
                <h3
                  style={{
                    color: "#ffffff",
                    fontSize: "18px",
                    marginTop: "4px",
                    marginBottom: "8px",
                  }}
                >
                  {selectedNode.name}/
                </h3>
                <p style={{ color: "#94a3b8", fontSize: "14px", lineHeight: "1.5" }}>
                  {selectedNode.desc}
                </p>
              </div>

              {/* Dissonance Quest Board Panel */}
              <div
                style={{
                  backgroundColor: "#07071f",
                  padding: "16px",
                  borderRadius: "6px",
                  border: "1px solid #1e1e38",
                }}
              >
                <h4
                  style={{
                    color: "#ef4444",
                    fontSize: "14px",
                    fontWeight: "bold",
                    textTransform: "uppercase",
                    marginBottom: "12px",
                    display: "flex",
                    alignItems: "center",
                    gap: "6px",
                  }}
                >
                  ⚠️ Active Dissonance Quests
                </h4>
                <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                  {dissonanceQuests.map((quest) => (
                    <div
                      key={quest.id}
                      style={{
                        padding: "12px",
                        backgroundColor: "#111130",
                        borderRadius: "4px",
                        borderLeft: "3px solid #ef4444",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          fontSize: "12px",
                        }}
                      >
                        <span style={{ color: "#94a3b8", fontWeight: "bold" }}>{quest.id}</span>
                        <span style={{ color: "#f87171", fontWeight: "bold" }}>
                          {quest.severity}
                        </span>
                      </div>
                      <p
                        style={{
                          color: "#f1f5f9",
                          fontSize: "13px",
                          marginTop: "4px",
                          marginBottom: "4px",
                        }}
                      >
                        {quest.title}
                      </p>
                      <span style={{ fontSize: "11px", color: "#64748b", fontFamily: "monospace" }}>
                        LOCUS: {quest.target}/
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Transmutation Cycle Transformation Screens */}
        {cyclePhase === "DISSONANCE" && (
          <div
            style={{
              height: "500px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor: "#1a0505",
              borderRadius: "8px",
              border: "2px dashed #ef4444",
              textAlign: "center",
            }}
          >
            <h2 style={{ color: "#f87171", fontSize: "28px" }}>
              PHASE 1: CRITICAL DISSONANCE DETECTED
            </h2>
            <p style={{ color: "#fca5a5", maxWidth: "500px", marginTop: "12px", fontSize: "15px" }}>
              Deconstructing active modules. Running Vector Safe Calculator to identify compliance
              deviation distance across system boundaries...
            </p>
          </div>
        )}

        {cyclePhase === "SYNTHESIS" && (
          <div
            style={{
              height: "500px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor: "#022c22",
              borderRadius: "8px",
              border: "2px solid #0d9488",
              textAlign: "center",
            }}
          >
            <h2 style={{ color: "#2dd4bf", fontSize: "28px" }}>
              PHASE 2: GENERATIVE TRANSFORMATION PROTOCOL
            </h2>
            <p style={{ color: "#99f6e4", maxWidth: "500px", marginTop: "12px", fontSize: "15px" }}>
              Weaving new structural connections via Implicit Synergy Engine. Compiling dynamic text
              logs directly into new Grand Playbook manifests...
            </p>
          </div>
        )}

        {cyclePhase === "TRANSCENDENCE" && (
          <div
            style={{
              height: "500px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor: "#1e1b4b",
              borderRadius: "8px",
              border: "2px solid #818cf8",
              textAlign: "center",
            }}
          >
            <h2 style={{ color: "#c7d2fe", fontSize: "28px" }}>
              PHASE 3: COHERENCE FLASH CRYSTALLIZATION
            </h2>
            <p style={{ color: "#e0e7ff", maxWidth: "500px", marginTop: "12px", fontSize: "15px" }}>
              Locking updated schemas securely to the master index registry. Mathematical
              integration complete. Returning to equilibrium safe vector.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default NetworkGraph;
