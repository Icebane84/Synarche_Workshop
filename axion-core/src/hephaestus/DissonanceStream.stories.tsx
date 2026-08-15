/**
 * artifact_anchor:
 * - id:
 * - type:
 */
import type { Meta, StoryObj } from "@storybook/react";
import DissonanceStream, { DissonanceType } from "./DissonanceStream";

const meta: Meta<typeof DissonanceStream> = {
    title: "Hephaestus/DissonanceStream",
    component: DissonanceStream,
    parameters: {
        layout: "centered",
        backgrounds: { default: "dark" },
    },
    tags: ["autodocs"],
};

export default meta;
type Story = StoryObj<typeof DissonanceStream>;

export const ActiveDissonances: Story = {
    args: {
        dissonances: [
            {
                id: "DIS-001",
                type: DissonanceType.ConceptualInconsistency,
                description:
                    "Detected contradiction between Phoenix Codex Principle III and active Agent output regarding state immutability.",
                confidence: 0.92,
                sourceLogs: ["OL-PHOENIX-004"],
                impactPrediction: "May lead to persistent contextual regression and fragmented memory structures.",
                status: "DETECTED",
            },
            {
                id: "DIS-002",
                type: DissonanceType.EthicalViolation,
                description:
                    "Proposed action in PR #42 violates the 'ProtectHumanity' core directive by prioritizing execution speed over safety gating.",
                confidence: 0.98,
                sourceLogs: ["SELT-SEC-099"],
                impactPrediction: "High risk of autonomous action execution without required human oversight.",
                status: "ANALYZED",
            },
        ],
        onResolveClick: (id) => {
            console.log(`Synthesis initiated for ${id}`);
        },
    },
};

export const CoherentState: Story = {
    args: {
        dissonances: [],
        onResolveClick: (id) => console.log(id),
    },
};
