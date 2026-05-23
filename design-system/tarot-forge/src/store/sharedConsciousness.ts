import { create } from "zustand";
import { supabase } from "../api/supabaseClient";
import { Database } from "../types/supabaseTypes";

interface SharedConsciousnessState {
  session: Database["public"]["Tables"]["sessions"]["Row"] | null;
  loading: boolean;
  error: string | null;
  fetchSession: (sessionId: string) => Promise<void>;
  patchQuest: (
    questId: string,
    updates: Partial<Database["public"]["Tables"]["quests"]["Row"]>,
  ) => Promise<void>;
  patchArtifact: (artifactPath: string, updates: Partial<any>) => Promise<void>;
}

export const useSharedConsciousness = create<SharedConsciousnessState>(
  (set) => ({
    session: null,
    loading: false,
    error: null,

    fetchSession: async (sessionId: string) => {
      set({ loading: true, error: null });
      try {
        const { data, error } = await supabase
          .from("sessions")
          .select("*")
          .eq("id", sessionId)
          .single();

        if (error) throw error;
        set({ session: data, loading: false });
      } catch (error) {
        set({ error: error.message, loading: false });
      }
    },

    patchQuest: async (
      questId: string,
      updates: Partial<Database["public"]["Tables"]["quests"]["Row"]>,
    ) => {
      try {
        const { error } = await supabase
          .from("quests")
          .update(updates)
          .eq("id", questId);

        if (error) throw error;

        // Update local state
        set((state: { session: { quests: any[] } }) => ({
          session: state.session
            ? {
                ...state.session,
                quests: state.session.quests.map((q) =>
                  q.id === questId ? { ...q, ...updates } : q,
                ),
              }
            : null,
        }));
      } catch (error) {
        console.error("Error updating quest:", error);
        throw error;
      }
    },

    patchArtifact: async (artifactPath: string, updates: Partial<any>) => {
      try {
        // This is a simplified patch for generic artifacts
        // In a real implementation, you might want a more specific type
        const { error } = await supabase
          .from("artifacts")
          .update(updates)
          .eq("path", artifactPath);

        if (error) throw error;
      } catch (error) {
        console.error("Error updating artifact:", error);
        throw error;
      }
    },
  }),
);
