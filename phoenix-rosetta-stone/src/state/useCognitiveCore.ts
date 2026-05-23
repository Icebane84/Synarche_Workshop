/** @fabric GVRN.Core.Fabric.State.Cognitive */

import type { ChatMessage } from "@essence/index";
import { supabase } from "@nexus/index";
import { create } from "zustand";

interface CognitiveState {
  // --- State: The Shared Consciousness ---
  messages: ChatMessage[];
  isLoading: boolean;
  coherenceIndex: number; // Real-time resonance metric (0.0 - 1.0)

  // --- Actions: State-modifying functions must live in the definition ---
  addMessage: (message: ChatMessage) => void;
  submitMessage: (text: string) => Promise<void>;
  setLoading: (status: boolean) => void;
  updateCoherence: (score: number) => void;
  resetConsciousness: () => void;
}

/**
 * Shared Consciousness Store
 * Performance: Selectors are mandatory for accessing state to prevent re-renders.
 */
export const useCognitiveCore = create<CognitiveState>((set, get) => ({
  messages: [],
  isLoading: false,
  coherenceIndex: 1.0, // Defaulting to perfect coherence

  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),

  submitMessage: async (text) => {
    // 1. Add User Message
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: "user",
      text,
    };
    set((state) => ({
      messages: [...state.messages, userMsg],
      isLoading: true,
    }));

    // Simulate cognitive strain
    const currentCoherence = get().coherenceIndex;
    set({ coherenceIndex: Math.max(0.1, currentCoherence - 0.08) });

    try {
      // 2. Call Supabase Edge Function for RAG / Gemini processing
      const { data, error } = await supabase.functions.invoke(
        "phoenix-cognitive-processor",
        {
          body: { prompt: text, history: get().messages },
        },
      );

      if (error) throw error;

      // 3. Add AI Response
      const aiMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: "ai",
        text: data.reply || "Cognitive synthesis achieved.",
      };
      set((state) => ({
        messages: [...state.messages, aiMsg],
        coherenceIndex: Math.min(1.0, state.coherenceIndex + 0.1), // Regain coherence
      }));
    } catch (err) {
      console.error("Transcendence Error:", err);
      // Fallback for when the Edge Function isn't deployed yet
      const fallbackMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: "ai",
        text: `[Edge Function Not Connected] I have received your prompt: "${text}". Waiting for backend integration.`,
      };
      set((state) => ({
        messages: [...state.messages, fallbackMsg],
        coherenceIndex: Math.min(1.0, state.coherenceIndex + 0.05),
      }));
    } finally {
      set({ isLoading: false });
    }
  },

  setLoading: (status) => set({ isLoading: status }),

  updateCoherence: (score) => set({ coherenceIndex: score }),

  resetConsciousness: () =>
    set({ messages: [], isLoading: false, coherenceIndex: 1.0 }),
}));
