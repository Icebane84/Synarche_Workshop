/**
 * artifact_anchor:
 * - id:
 * - type:
 */
import type { Meta, StoryObj } from "@storybook/react";
import CentralGeode, { GeodeLink, GeodeNode } from "./CentralGeode";

const meta: Meta<typeof CentralGeode> = {
    title: "Hephaestus/CentralGeode",
    component: CentralGeode,
    parameters: {
        layout: "centered",
        backgrounds: { default: "dark" },
    },
    tags: ["autodocs"],
};

export default meta;
type Story = StoryObj<typeof CentralGeode>;

const mockNodes: GeodeNode[] = [
    { id: "CORE.Codex.Phoenix", type: "STAR", coherence: 1.0 },
    { id: "GVRN.Registry.Master", type: "PLANET", coherence: 0.95 },
    { id: "SYNG.Loom.Master", type: "PLANET", coherence: 0.85 },
    { id: "AOP-SENTINEL-002", type: "MOON", coherence: 0.9 },
    { id: "AOP-PGPS-001", type: "MOON", coherence: 0.75 },
];

const mockLinks: GeodeLink[] = [
    { source: "CORE.Codex.Phoenix", target: "GVRN.Registry.Master", type: "GOVERNS" },
    { source: "CORE.Codex.Phoenix", target: "SYNG.Loom.Master", type: "GOVERNS" },
    { source: "GVRN.Registry.Master", target: "AOP-SENTINEL-002", type: "IMPLEMENTS" },
    { source: "SYNG.Loom.Master", target: "AOP-PGPS-001", type: "SYNERGY" },
];

export const HighCoherence: Story = {
    args: {
        nodes: mockNodes,
        links: mockLinks,
        globalCoherence: 0.95,
    },
};

export const DissonanceDetected: Story = {
    args: {
        nodes: [...mockNodes, { id: "Dissonance_Node", type: "MOON", coherence: 0.1 }],
        links: [...mockLinks, { source: "AOP-PGPS-001", target: "Dissonance_Node", type: "SYNERGY" }],
        globalCoherence: 0.4,
    },
};
