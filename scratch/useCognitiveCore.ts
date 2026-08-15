import { z } from 'zod';
import { create } from 'zustand';
import {
	CognitiveCoreStateSchema,
	LegacyTalentSchema,
	LegendaryAchievementSchema,
} from '../where_light_fades/GAME.Schema.CognitiveCore'; // Adjusted path

// --- Type Definitions inferred from Zod Schemas ---

/**
 * The state shape of the Cognitive Core, inferred directly from the Zod schema.
 * This ensures the TypeScript type and the runtime validation are always in sync.
 */
export type CognitiveCoreState = z.infer<typeof CognitiveCoreStateSchema>;
export type LegendaryAchievement = z.infer<typeof LegendaryAchievementSchema>;
export type LegacyTalent = z.infer<typeof LegacyTalentSchema>;

export interface CognitiveCoreActions {
  completeLegendaryAchievement: (achievementId: string) => void;
  initiatePrestigeReset: (talentId: string) => { success: boolean; message: string };
  loadInitialData: (data: {
    legendaryAchievements: LegendaryAchievement[];
    legacyTalents: LegacyTalent[];
  }) => void;
}

export type CognitiveCoreStore = CognitiveCoreState & CognitiveCoreActions;

// The initial state must conform to the Zod schema.
const initialState: CognitiveCoreState = {
	prestigeLevel: 0,
	characterLevel: 1,
	skillPoints: 0,
	legendaryAchievements: [],
	legacyTalents: [],
	playerAchievements: [],
	unlockedLegacyTalents: [],
};

const useCognitiveCore = create<CognitiveCoreStore>((set, get) => ({
  ...initialState,
  // --- Actions ---

  /**
   * Loads static data like available achievements and talents into the store.
   */
  loadInitialData: (data) => {
    // Validate the incoming data against a partial schema.
    const result = CognitiveCoreStateSchema.partial().safeParse(data);

    if (!result.success) {
      console.error('[CognitiveCore] Failed to load initial data due to validation errors:', result.error.issues);
      return; // Abort state update
    }

    // Proceed with the validated data
    const { legendaryAchievements, legacyTalents } = result.data;

    if (!legendaryAchievements || !legacyTalents) return;

    const playerAchievements = legendaryAchievements.map((ach: { id: any; }) => ({
      achievementId: ach.id,
      isCompleted: false,
      completedTimestamp: null,
    }));

    set({ legendaryAchievements, legacyTalents, playerAchievements });
  },

  /**
   * Validates and processes the completion of a legendary achievement.
   * Awards non-grindable Prestige Points (PP).
   */
  completeLegendaryAchievement: (achievementId: string) => {
    const state = get();
    const playerAch = state.playerAchievements.find((pa) => pa.achievementId === achievementId);

    if (!playerAch || playerAch.isCompleted) {
      console.warn(`Achievement ${achievementId} already completed or does not exist.`);
      return;
    }

    const achievementData = state.legendaryAchievements.find((la) => la.id === achievementId);
    if (!achievementData) {
      console.error(`Data for legendary achievement ${achievementId} not found.`);
      return;
    }

    set((prevState) => ({
      prestigeLevel: prevState.prestigeLevel + achievementData.ppValue,
      playerAchievements: prevState.playerAchievements.map((pa) =>
        pa.achievementId === achievementId
          ? { ...pa, isCompleted: true, completedTimestamp: Date.now() }
          : pa
      ),
    }));
  },

  /**
   * Implements the "Rebirth" mechanic. Resets character progress to unlock
   * a permanent, account-wide Legacy Talent.
   */
  initiatePrestigeReset: (talentId: string) => {
    const state = get();
    if (state.unlockedLegacyTalents.length >= 15) {
      return { success: false, message: 'Prestige cap reached. Maximum of 15 talents unlocked.' };
    }

    const talent = state.legacyTalents.find((t) => t.id === talentId);
    if (!talent) {
      return { success: false, message: `Legacy Talent with ID "${talentId}" not found.` };
    }

    if (state.unlockedLegacyTalents.includes(talentId)) {
      return { success: false, message: `Legacy Talent "${talent.name}" is already unlocked.` };
    }

    if (state.prestigeLevel < talent.cost) {
      return { success: false, message: `Insufficient Prestige Points. Requires ${talent.cost}, but you only have ${state.prestigeLevel}.` };
    }

    set((prevState) => ({
      prestigeLevel: prevState.prestigeLevel - talent.cost,
      characterLevel: 1,
      skillPoints: 0,
      unlockedLegacyTalents: [...prevState.unlockedLegacyTalents, talentId],
      // Clears dynamic achievement states for re-earning, as per the spec
      playerAchievements: prevState.playerAchievements.map((pa) => ({ ...pa, isCompleted: false, completedTimestamp: null })),
    }));

    return { success: true, message: `Rebirth complete! Legacy Talent "${talent.name}" unlocked.` };
  },
}));

export default useCognitiveCore;