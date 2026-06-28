/**
 * @artifact phoenix-rosetta-stone/src/core/useUserContext.ts
 * Zustand store for the Chris / Axion user context switcher.
 * All hooks that need a user_id pull from here.
 */

import { create } from "zustand";

// The two sovereign users of the Synarche
export type SynarchemUser = "Chris" | "Axion";

// These UUIDs map to player_state.user_id in Supabase.
// Update these once the rows are seeded.
export const USER_IDS: Record<SynarchemUser, string> = {
  Chris: "00000000-0000-0000-0000-000000000001",
  Axion: "00000000-0000-0000-0000-000000000002",
};

// Visual theme per user — drives CSS accent colors throughout the HUD
export const USER_THEME: Record<SynarchemUser, {
  accent: string;
  glowClass: string;
  borderClass: string;
  textClass: string;
  bgClass: string;
}> = {
  Chris: {
    accent: "#f59e0b",
    glowClass: "glow-amber",
    borderClass: "border-chris-amber/40",
    textClass: "text-chris-amber",
    bgClass: "bg-chris-amber/10",
  },
  Axion: {
    accent: "#6366f1",
    glowClass: "glow-indigo",
    borderClass: "border-axion-indigo/40",
    textClass: "text-axion-indigo",
    bgClass: "bg-axion-indigo/10",
  },
};

interface UserContextState {
  activeUser: SynarchemUser;
  userId: string;
  setUser: (user: SynarchemUser) => void;
}

export const useUserContext = create<UserContextState>((set) => ({
  activeUser: "Chris",
  userId: USER_IDS.Chris,
  setUser: (user) => set({ activeUser: user, userId: USER_IDS[user] }),
}));
