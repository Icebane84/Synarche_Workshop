import type { Meta, StoryObj } from "@storybook/react";
import { PhoenixGeode } from "./PhoenixGeode";

const meta: Meta<typeof PhoenixGeode> = {
  title: "Fabric (UI Layer)/PhoenixGeode", // Master Star-Chart Categorization
  component: PhoenixGeode,
  parameters: {
    layout: "centered",
    backgrounds: {
      default: "Nebula Void",
      values: [
        { name: "Nebula Void", value: "#00001a" },
        { name: "Deep Space", value: "#23272A" },
      ],
    },
    docs: {
      description: {
        component:
          "The central visualization of the AI's internal state. It uses D3.js to render a rotating, pulsing crystalline structure that physically reacts to the system's Coherence Index.",
      },
    },
  },
  decorators: [
    (Story) => (
      <div className="w-[400px] h-[400px] flex items-center justify-center">
        <Story />
      </div>
    ),
  ],
  argTypes: {
    coherenceIndex: {
      control: { type: "range", min: 0, max: 10, step: 1 },
      description:
        "The current cognitive coherence of the system. Higher values increase the size, glow, and complexity of the geode.",
    },
  },
};

export default meta;

type Story = StoryObj<typeof PhoenixGeode>;

export const LowCoherence: Story = {
  args: {
    coherenceIndex: 1,
  },
  parameters: {
    docs: {
      description: {
        story:
          "The state of the system when it is highly disjointed. The geode is small, dim, and rotating slowly.",
      },
    },
  },
};

export const ModerateCoherence: Story = {
  args: {
    coherenceIndex: 5,
  },
};

export const HighCoherence: Story = {
  args: {
    coherenceIndex: 9,
  },
  parameters: {
    docs: {
      description: {
        story:
          "The state of the system when cognitive alignment is achieved. The geode expands, glows intensely with Luminous Coherence, and rotates dynamically.",
      },
    },
  },
};
