import type { Meta, StoryObj } from "@storybook/react";
import { ChatInterface } from "./ChatInterface";
import type { ChatMessage } from "@essence/index";

const meta: Meta<typeof ChatInterface> = {
  title: "Fabric (UI Layer)/ChatInterface", // Master Star-Chart Categorization
  component: ChatInterface,
  parameters: {
    layout: "padded",
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
          "The Scriptorium. This is the primary interface for the Conductor to weave commands into the AI's cognitive loop. It features dynamic glassmorphic Tarot-card aesthetics.",
      },
    },
  },
  decorators: [
    (Story) => (
      <div className="h-[600px] w-full max-w-2xl bg-black/40 backdrop-blur-xl border border-white/5 rounded-2xl overflow-hidden shadow-[0_0_40px_rgba(119,181,254,0.15)] relative">
        <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-celestial-blue/30 to-transparent" />
        <Story />
      </div>
    ),
  ],
  argTypes: {
    onSubmit: { action: "submitted" },
  },
};

export default meta;

type Story = StoryObj<typeof ChatInterface>;

const sampleMessages: ChatMessage[] = [
  {
    id: "1",
    sender: "user",
    text: "What is the purpose of the Phoenix Protocol?",
  },
  {
    id: "2",
    sender: "ai",
    text: "The Phoenix Protocol is the complete architectural blueprint for the Rosetta Stone application.",
  },
];

export const Empty: Story = {
  args: {
    messages: [],
    isLoading: false,
  },
};

export const ActiveConversation: Story = {
  args: {
    messages: sampleMessages,
    isLoading: false,
  },
};

export const Synthesizing: Story = {
  args: {
    messages: sampleMessages,
    isLoading: true,
  },
};
