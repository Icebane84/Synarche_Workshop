import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { useCognitiveCore } from './useCognitiveCore';

/**
 * A specialized visualization component for the Cognitive Component Storybook (CCS).
 * This component exists solely to visualize the invisible state changes of the
 * useCognitiveCore Zustand store, fulfilling the "Visualization of the Invisible"
 * requirement for Explainable AI (XAI).
 */
const CognitiveStoreVisualizer = () => {
  const { 
    messages, 
    coherenceIndex, 
    isProcessing, 
    submitMessage 
  } = useCognitiveCore();

  // Utility to fire a test message into the store
  const handleTestStimulus = () => {
    submitMessage("Analyze the systemic dissonance.");
  };

  return (
    <div className="p-8 bg-black/80 backdrop-blur-md rounded-2xl border border-white/10 text-white font-mono text-sm max-w-3xl">
      <h2 className="text-xl text-celestial-blue mb-6 tracking-widest uppercase border-b border-white/10 pb-4">
        Cognitive Core: State Visualization
      </h2>
      
      <div className="grid grid-cols-2 gap-8">
        {/* Left Column: Metrics */}
        <div className="space-y-6">
          <div>
            <h3 className="text-white/50 text-xs uppercase mb-2">Coherence Index</h3>
            <div className="flex items-center space-x-4">
              <div className="text-4xl font-light text-coherence-indigo">
                {coherenceIndex.toFixed(1)}
              </div>
              <div className="flex-grow h-2 bg-white/10 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-coherence-indigo transition-all duration-1000"
                  style={{ width: `${(coherenceIndex / 10) * 100}%` }}
                />
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-white/50 text-xs uppercase mb-2">Processing Status</h3>
            <div className={`px-3 py-1 rounded text-xs inline-block ${
              isProcessing 
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30 animate-pulse' 
                : 'bg-green-500/20 text-green-300 border border-green-500/30'
            }`}>
              {isProcessing ? 'SYNTHESIZING...' : 'IDLE'}
            </div>
          </div>

          <div className="pt-4 border-t border-white/10">
            <h3 className="text-white/50 text-xs uppercase mb-2">Metacognitive Controls</h3>
            <button 
              onClick={handleTestStimulus}
              disabled={isProcessing}
              className="px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded transition-colors disabled:opacity-50 text-xs"
            >
              Inject Test Stimulus
            </button>
          </div>
        </div>

        {/* Right Column: Internal Log */}
        <div>
          <h3 className="text-white/50 text-xs uppercase mb-2">Internal Message Buffer ({messages.length})</h3>
          <div className="h-64 overflow-y-auto bg-black/50 border border-white/5 rounded p-4 space-y-3 scrollbar-thin scrollbar-thumb-white/10">
            {messages.length === 0 ? (
              <div className="text-white/30 italic text-xs">Buffer empty.</div>
            ) : (
              messages.map(msg => (
                <div key={msg.id} className="border-l-2 border-white/20 pl-3">
                  <div className="text-[10px] text-white/40 uppercase">
                    {msg.sender === 'user' ? 'STIMULUS (USER)' : 'RESPONSE (SYS)'}
                  </div>
                  <div className="text-xs text-white/80 mt-1 truncate">
                    {msg.text}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const meta: Meta<typeof CognitiveStoreVisualizer> = {
  title: 'Nexus (Cognitive Layer)/CognitiveCore', // Master Star-Chart Categorization
  component: CognitiveStoreVisualizer,
  parameters: {
    layout: 'centered',
    backgrounds: {
      default: 'Deep Space',
      values: [
        { name: 'Nebula Void', value: '#00001a' },
        { name: 'Deep Space', value: '#23272A' },
      ],
    },
    docs: {
      description: {
        component: "Visualization of the Invisible. This story acts as a diagnostic window into the `useCognitiveCore` Zustand store, fulfilling the XAI requirement for metacognitive observation.",
      },
    },
  },
};

export default meta;

type Story = StoryObj<typeof CognitiveStoreVisualizer>;

export const StateObservation: Story = {};
