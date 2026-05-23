/**
 * ==========================================
 * SYNARCHE SOVEREIGN METADATA (UIP-V15)
 * ==========================================
 * ARTIFACT ID: SYNG.UI.LOGIC.Synapse
 * Domain: UI/UX | State: ACTIVE | Criticality: HIGH
 * Objective: Manage state, relational gravity, and superposition math for the Cognitive Loom UI.
 * Relations: IMPLEMENTS: ARCH.VIS.LoomVisualizer
 *
 *[OMNI-ARTIFACT-ANCHOR] ID: SYNG.UI.LOGIC.Synapse VER: v15.0 [OMEGA] STATUS: ACTIVE TS: 2026-04-22
 */

import { useState, useCallback, useMemo } from "react";

// --- I. SOVEREIGN TYPE DEFINITIONS ---

export type CelestialClass = "STAR" | "PLANET" | "MOON" | "ASTEROID" | "VOID";
export type RelationType =
  | "GOVERNS"
  | "IMPLEMENTS"
  | "UTILIZES"
  | "INDEXES"
  | "SYNERGY";

export interface StateVector {
  coherence: number; // 0.0 to 1.0
  resonance: number; // 0.0 to 1.0
  stability: "Stable" | "Eternal" | "Volatile" | "Degraded";
}

export interface SynergyEdge {
  id: string;
  source: string; // Artifact ID
  target: string; // Artifact ID
  relationType: RelationType;
  weight: number; // Relational Gravity
}

export interface SynapseNode {
  id: string;
  label: string;
  celestialClass: CelestialClass;
  stateVector: StateVector;
  superposition: [number, number, number]; // [x, y, z] spatial probability vectors
  isFocused: boolean;
}

// --- II. THE SYNAPSE HOOK (CORE LOGIC) ---

export const useSynapseLogic = (
  initialNodes: SynapseNode[],
  initialEdges: SynergyEdge[],
) => {
  const [nodes, setNodes] = useState<SynapseNode[]>(initialNodes);
  const [edges, setEdges] = useState<SynergyEdge[]>(initialEdges);
  const [activeFocus, setActiveFocus] = useState<string | null>(null);

  /**
   * PHASE 1: SUPERPOSITION CALCULUS
   * Calculates the probabilistic spatial coordinates of nodes based on their State Vector.
   * High Coherence pulls nodes toward the Z-axis (Foreground).
   */
  const calculateSuperposition = useCallback(() => {
    setNodes((prevNodes) =>
      prevNodes.map((node) => {
        const gravityPull = node.stateVector.coherence * 10;
        const resonanceShift = node.stateVector.resonance * Math.random() * 5; // Simulates particle jitter

        return {
          ...node,
          superposition: [
            node.superposition[0] + resonanceShift,
            node.superposition[1],
            node.stateVector.coherence >= 0.9
              ? 100
              : node.superposition[2] - gravityPull,
          ],
        };
      }),
    );
  }, []);

  /**
   * PHASE 2: WAVEFORM COLLAPSE
   * When a node is "observed" (clicked/hovered), its superposition collapses.
   * Linked nodes are pulled into its orbit based on edge weight.
   */
  const collapseSuperposition = useCallback(
    (targetId: string) => {
      setActiveFocus(targetId);

      setNodes((prevNodes) =>
        prevNodes.map((node) => {
          const isTarget = node.id === targetId;
          const directEdge = edges.find(
            (e) =>
              (e.source === targetId && e.target === node.id) ||
              (e.target === targetId && e.source === node.id),
          );

          if (isTarget) {
            // Center the observed node
            return { ...node, isFocused: true, superposition: [0, 0, 200] };
          } else if (directEdge) {
            // Orbit the observed node based on Relational Gravity
            const orbitRadius = 100 / directEdge.weight;
            return {
              ...node,
              isFocused: false,
              superposition: [orbitRadius, orbitRadius, 150],
            };
          } else {
            // Push unrelated nodes to the Void
            return {
              ...node,
              isFocused: false,
              superposition: [
                node.superposition[0] * 2,
                node.superposition[1] * 2,
                -100,
              ],
            };
          }
        }),
      );
    },
    [edges],
  );

  /**
   * PHASE 3: ENTROPY PURGE
   * Clears focus and scatters nodes back into their standard entropic distribution.
   */
  const resetMatrix = useCallback(() => {
    setActiveFocus(null);
    setNodes(initialNodes); // Reset to base state vectors
  }, [initialNodes]);

  return {
    nodes,
    edges,
    activeFocus,
    calculateSuperposition,
    collapseSuperposition,
    resetMatrix,
  };
};
