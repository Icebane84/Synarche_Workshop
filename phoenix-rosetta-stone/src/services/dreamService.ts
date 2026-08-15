import { useCoherenceStore } from '../store/coherenceStore';

/**
 * @fileoverview The Dream Service.
 * This sovereign module handles the "Background Dreaming" logic.
 * When the system is idle, it performs simulated "Garbage Collection" and "Synaptic Pruning",
 * which translates to optimizing internal stats and cleaning up logs.
 */

const DREAM_LOGS = [
    "Optimizing neural pathways in Sector 7...",
    "Pruning low-relevance synaptic connections...",
    "Re-indexing archival memories for faster retrieval...",
    "Simulating potential futures (Synergy Search)...",
    "Defragmenting the Logic Matrix...",
    "Harmonizing dissonance echoes from previous session...",
    "Analyzing user interaction patterns for adaptive response..."
];

const getRandomFloat = (): number => {
  const array = new Uint32Array(1);
  crypto.getRandomValues(array);
  return array[0] / (0xffffffff + 1);
};

/**
 * Executes a single "REM Cycle" (Rapid Eye Movement).
 * This function is called periodically while the system is in the Dreaming state.
 */
export const executeRemCycle = () => {
    const store = useCoherenceStore.getState();

    // 1. Simulate "Thought"
    const dreamThought = DREAM_LOGS[Math.floor(getRandomFloat() * DREAM_LOGS.length)];

    // 2. Apply Benefit (Garbage Collection Reward)
    if (getRandomFloat() > 0.8) {
        store.addNovaSpark(`[DREAM] ${dreamThought} (Coherence Stabilized)`);
        store.pulse(); // Visual feedback
    }
};