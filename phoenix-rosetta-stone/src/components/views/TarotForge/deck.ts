export interface TarotCard {
    id: string;
    number: number;
    name: string;
    title: string;
    archetype: string;
    domain: string;
    color: string;
    bgGlow: string;
    border: string;
    description: string;
    abilities: string[];
    resonance: number;
    activeMask: string;
}

export const TAROT_DECK: TarotCard[] = [
    {
        id: "THE_SOVEREIGN",
        number: 0,
        name: "The Sovereign",
        title: "Master Artificer of Synarche",
        archetype: "AXION KERNEL",
        domain: "CORE",
        color: "text-amber-400",
        bgGlow: "shadow-amber-500/20 bg-amber-500/10",
        border: "border-amber-500/40",
        description:
            "Architect of zero-entropy coherence, enforcing strict memory-mapped execution frames and systemic alignment across the workspace.",
        abilities: [
            "Memory-Mapped SCC Solving",
            "Tarjan Dependency Graph Partitioning",
            "Zero-Entropy Invalidation Waves",
        ],
        resonance: 0.98,
        activeMask: "[The Sovereign]",
    },
    {
        id: "THE_MAGICIAN",
        number: 1,
        name: "The Magician",
        title: "Master Transmuter & Ingestion Specialist",
        archetype: "TRANSFORMER",
        domain: "INGEST",
        color: "text-purple-400",
        bgGlow: "shadow-purple-500/20 bg-purple-500/10",
        border: "border-purple-500/40",
        description:
            "Transmutes raw data, documentation, and external URLs into clean knowledge matrices and structured markdown nodes.",
        abilities: ["Magician Ingestion Matrix", "AST Transformation Protocols", "Knowledge Graph Embedding Sync"],
        resonance: 0.95,
        activeMask: "[The Magician]",
    },
    {
        id: "THE_HIGH_PRIESTESS",
        number: 2,
        name: "The High Priestess",
        title: "Keeper of the Cognitive Loom & Wisdom",
        archetype: "SOPHIA WISDOM",
        domain: "EPISTEMIC",
        color: "text-indigo-400",
        bgGlow: "shadow-indigo-500/20 bg-indigo-500/10",
        border: "border-indigo-500/40",
        description:
            "Navigates multi-tier memory layers (L1–L9) and maintains the Cognitive Memory Palace through semantic resonance.",
        abilities: [
            "L1–L9 Memory Layer Traversal",
            "Cognitive Loom Uncertainty Protocol",
            "Vector Similarity Synthesis",
        ],
        resonance: 0.94,
        activeMask: "[The High Priestess]",
    },
    {
        id: "THE_STAR",
        number: 17,
        name: "The Star",
        title: "Beacon of Hope & Visual Harmony",
        archetype: "AESTHETIC FORGE",
        domain: "FRONTEND",
        color: "text-celestial-blue",
        bgGlow: "shadow-celestial-blue/20 bg-celestial-blue/10",
        border: "border-celestial-blue/40",
        description:
            "Crafts stunning modern interfaces with vibrant glassmorphism, fluid micro-animations, and pristine visual feedback.",
        abilities: ["State-of-the-Art UI Design", "Dynamic Micro-Animations", "Tailwind Design Token Weaver"],
        resonance: 0.99,
        activeMask: "[The Star]",
    },
    {
        id: "THE_SENTINEL",
        number: 20,
        name: "The Sentinel",
        title: "Guardian of Governance & Conscience",
        archetype: "AUDIT ENGINE",
        domain: "GVRN",
        color: "text-red-400",
        bgGlow: "shadow-red-500/20 bg-red-500/10",
        border: "border-red-500/40",
        description:
            "Continuously scans workspace artifacts for structural, semantic, and operational dissonance, enforcing Law 00 compliance.",
        abilities: ["Real-Time Dissonance Scanning", "Refinement Quest Auto-Generation", "Lexicon Boundary Enforcer"],
        resonance: 0.96,
        activeMask: "[The Sentinel]",
    },
];
