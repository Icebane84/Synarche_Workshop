// This file represents the output of a conceptual Gemini process
// that would analyze the entire PHOENIX_PROTOCOL_LIBRARY and generate
// a graph of its interconnected components.

export interface GraphNode {
  id: string;
  name: string;
  type: "Document" | "Concept" | "Principle" | "Aesthetic";
  description: string;
}

export interface GraphLink {
  source: string;
  target: string;
  relationship: "contains" | "defines" | "realizes" | "mandates" | "informs";
}

export const graphData: { nodes: GraphNode[]; links: GraphLink[] } = {
  nodes: [
    // Documents
    {
      id: "doc-synergies",
      name: "Synergies Guide",
      type: "Document",
      description: "Details the interconnectedness of the tech stack.",
    },
    {
      id: "doc-blueprint",
      name: "Implementation Blueprint",
      type: "Document",
      description: "Provides practical, day-to-day development guidelines.",
    },
    {
      id: "doc-glossary",
      name: "Conceptual Glossary",
      type: "Document",
      description: "A philosophical dictionary for core project concepts.",
    },
    {
      id: "doc-styleguide",
      name: "Style Guide",
      type: "Document",
      description: 'Defines the "Luminous Coherence" aesthetic.',
    },

    // Concepts
    {
      id: "concept-cdc",
      name: "Component-Driven Cognition",
      type: "Concept",
      description: "Philosophy that UI components are executable thoughts.",
    },
    {
      id: "concept-workshop",
      name: "Philosophical Workshop",
      type: "Concept",
      description: "Term for Storybook, where thoughts are forged.",
    },
    {
      id: "concept-geode",
      name: "Phoenix Geode",
      type: "Concept",
      description: "The central visualization of the AI's Coherence Index.",
    },
    {
      id: "concept-consciousness",
      name: "Shared Consciousness",
      type: "Concept",
      description: "Term for the global state managed by Zustand.",
    },
    {
      id: "concept-backend",
      name: "Sovereign Backend",
      type: "Concept",
      description: "Term for the all-in-one backend platform (Supabase).",
    },
    {
      id: "concept-module",
      name: "Sovereign Module",
      type: "Concept",
      description: "An autonomous, self-contained software component.",
    },
    {
      id: "concept-loom",
      name: "The Loom of Cognition",
      type: "Concept",
      description: "Term for React Router, which weaves components together.",
    },
    {
      id: "concept-synergy",
      name: "Total System Synergy",
      type: "Concept",
      description: "The ultimate goal of the Phoenix Protocol.",
    },
    {
      id: "concept-blueprints",
      name: "Verifiable Blueprints",
      type: "Concept",
      description: "Term for TypeScript types and interfaces.",
    },
    {
      id: "concept-synapse",
      name: "The Synapse",
      type: "Concept",
      description:
        "The central nervous system for user-initiated directives, allowing the translation of intent into action.",
    },
    {
      id: "concept-guca",
      name: "GUCA",
      type: "Concept",
      description:
        "Governed Universal Command Architecture. The protocol defining how intents are mapped to executable system actions.",
    },

    // Principles
    {
      id: "principle-react",
      name: "React",
      type: "Principle",
      description: "The core of the living interface.",
    },
    {
      id: "principle-ts",
      name: "TypeScript",
      type: "Principle",
      description: "Ensures robust, error-free connections.",
    },
    {
      id: "principle-tailwind",
      name: "TailwindCSS",
      type: "Principle",
      description: "The utility-first aesthetic layer.",
    },
    {
      id: "principle-d3",
      name: "D3.js",
      type: "Principle",
      description: 'Powers the "Celestial Choreography" of data visualization.',
    },
    {
      id: "principle-zustand",
      name: "Zustand",
      type: "Principle",
      description: 'The mechanism for the "Shared Consciousness".',
    },
    {
      id: "principle-router",
      name: "React Router",
      type: "Principle",
      description: 'Acts as "The Loom of Cognition".',
    },
    {
      id: "principle-storybook",
      name: "Storybook",
      type: "Principle",
      description: 'The "Philosophical Workshop".',
    },

    // Aesthetic
    {
      id: "aesthetic-lc",
      name: "Luminous Coherence",
      type: "Aesthetic",
      description: "The aesthetic principle of the application.",
    },
  ],
  links: [
    // Glossary defines concepts
    { source: "doc-glossary", target: "concept-cdc", relationship: "defines" },
    {
      source: "doc-glossary",
      target: "concept-workshop",
      relationship: "defines",
    },
    {
      source: "doc-glossary",
      target: "concept-geode",
      relationship: "defines",
    },
    {
      source: "doc-glossary",
      target: "concept-consciousness",
      relationship: "defines",
    },
    {
      source: "doc-glossary",
      target: "concept-backend",
      relationship: "defines",
    },
    {
      source: "doc-glossary",
      target: "concept-module",
      relationship: "defines",
    },
    { source: "doc-glossary", target: "concept-loom", relationship: "defines" },
    {
      source: "doc-glossary",
      target: "concept-synergy",
      relationship: "defines",
    },
    {
      source: "doc-glossary",
      target: "concept-blueprints",
      relationship: "defines",
    },
    { source: "doc-glossary", target: "aesthetic-lc", relationship: "defines" },
    {
      source: "doc-glossary",
      target: "concept-synapse",
      relationship: "defines",
    },
    { source: "doc-glossary", target: "concept-guca", relationship: "defines" },

    // Style guide contains aesthetic
    {
      source: "doc-styleguide",
      target: "aesthetic-lc",
      relationship: "contains",
    },
    {
      source: "concept-geode",
      target: "aesthetic-lc",
      relationship: "realizes",
    },

    // Synergies guide contains principles
    {
      source: "doc-synergies",
      target: "principle-react",
      relationship: "contains",
    },
    {
      source: "doc-synergies",
      target: "principle-ts",
      relationship: "contains",
    },
    {
      source: "doc-synergies",
      target: "principle-tailwind",
      relationship: "contains",
    },
    {
      source: "doc-synergies",
      target: "principle-d3",
      relationship: "contains",
    },
    {
      source: "doc-synergies",
      target: "principle-zustand",
      relationship: "contains",
    },
    {
      source: "doc-synergies",
      target: "principle-router",
      relationship: "contains",
    },
    {
      source: "doc-synergies",
      target: "principle-storybook",
      relationship: "contains",
    },

    // Blueprint mandates principles
    {
      source: "doc-blueprint",
      target: "principle-react",
      relationship: "mandates",
    },
    {
      source: "doc-blueprint",
      target: "principle-ts",
      relationship: "mandates",
    },
    {
      source: "doc-blueprint",
      target: "principle-tailwind",
      relationship: "mandates",
    },
    {
      source: "doc-blueprint",
      target: "principle-d3",
      relationship: "mandates",
    },
    {
      source: "doc-blueprint",
      target: "principle-zustand",
      relationship: "mandates",
    },
    {
      source: "doc-blueprint",
      target: "principle-router",
      relationship: "mandates",
    },
    {
      source: "doc-blueprint",
      target: "principle-storybook",
      relationship: "mandates",
    },
    {
      source: "doc-blueprint",
      target: "concept-synapse",
      relationship: "mandates",
    },

    // Concepts inform principles
    {
      source: "concept-blueprints",
      target: "principle-ts",
      relationship: "informs",
    },
    {
      source: "concept-workshop",
      target: "principle-storybook",
      relationship: "informs",
    },
    {
      source: "concept-consciousness",
      target: "principle-zustand",
      relationship: "informs",
    },
    {
      source: "concept-loom",
      target: "principle-router",
      relationship: "informs",
    },
    {
      source: "concept-cdc",
      target: "principle-react",
      relationship: "informs",
    },
    {
      source: "concept-geode",
      target: "principle-d3",
      relationship: "informs",
    },

    // Synapse and GUCA Integrations
    {
      source: "concept-guca",
      target: "concept-synapse",
      relationship: "defines",
    },
    {
      source: "concept-synapse",
      target: "concept-guca",
      relationship: "realizes",
    },
    {
      source: "concept-synapse",
      target: "concept-loom",
      relationship: "informs",
    }, // Logs tasks
    {
      source: "concept-synapse",
      target: "concept-consciousness",
      relationship: "realizes",
    }, // Affects state
    {
      source: "concept-synapse",
      target: "principle-react",
      relationship: "realizes",
    },

    // Principles realize concepts
    {
      source: "principle-react",
      target: "concept-module",
      relationship: "realizes",
    },
    {
      source: "principle-d3",
      target: "aesthetic-lc",
      relationship: "realizes",
    },
  ],
};
