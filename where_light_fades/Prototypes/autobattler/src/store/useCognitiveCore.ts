import { z } from 'zod';
import { create } from 'zustand';
import {
	CognitiveCoreStateSchema,
	LegacyTalentSchema,
	LegendaryAchievementSchema,
} from './GAME.Schema.CognitiveCore';

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

const initialState: CognitiveCoreState = {
	prestigeLevel: 0,
	characterLevel: 1,
	skillPoints: 0,
	legendaryAchievements: [
		{
			id: 'ach-1',
			name: 'Oakhaven Purified',
			description: 'Defeat the Ashen Abomination at the Oakhaven Chapel.',
			ppValue: 10
		},
		{
			id: 'ach-2',
			name: "Sentinel's Gambit",
			description: "Trigger Garrett's stun to intercept a fatal recoil strike.",
			ppValue: 15
		},
		{
			id: 'ach-3',
			name: 'Inner Sanctuary',
			description: 'Reach maximum flame stability with Serafina.',
			ppValue: 20
		}
	],
	legacyTalents: [
		{
			id: 'talent-1',
			name: 'Eternal Ember',
			description: 'Regenerate +2 Inner Flame automatically on every cycle.',
			cost: 10,
			tier: 'Tier 1'
		},
		{
			id: 'talent-2',
			name: 'Alerion Reflexes',
			description: "Garrett's attacks apply +2 Exposed stacks per hit.",
			cost: 15,
			tier: 'Tier 1'
		},
		{
			id: 'talent-3',
			name: "Warden's Grace",
			description: 'Serafina passive shield absorbs 30% more recoil damage.',
			cost: 20,
			tier: 'Tier 2'
		},
		{
			id: 'talent-4',
			name: "Eldrin's Grace",
			description: 'Precision deflection reduces recoil bleedthrough by 60%. Unlocked in Inner World.',
			cost: 25,
			tier: 'Tier 2'
		}
	],
	playerAchievements: [
		{ achievementId: 'ach-1', isCompleted: false, completedTimestamp: null },
		{ achievementId: 'ach-2', isCompleted: false, completedTimestamp: null },
		{ achievementId: 'ach-3', isCompleted: false, completedTimestamp: null }
	],
	unlockedLegacyTalents: [],
};

export const useCognitiveCore = create<CognitiveCoreStore>((set, get) => ({
  ...initialState,

  loadInitialData: (data) => {
    const result = CognitiveCoreStateSchema.partial().safeParse(data);
    if (!result.success) {
      console.error('[CognitiveCore] Validation errors:', result.error.issues);
      return;
    }
    const { legendaryAchievements, legacyTalents } = result.data;
    if (!legendaryAchievements || !legacyTalents) return;

    const playerAchievements = legendaryAchievements.map((ach) => ({
      achievementId: ach.id,
      isCompleted: false,
      completedTimestamp: null,
    }));

    set({ legendaryAchievements, legacyTalents, playerAchievements });
  },

  completeLegendaryAchievement: (achievementId: string) => {
    const state = get();
    const playerAch = state.playerAchievements.find((pa) => pa.achievementId === achievementId);

    if (!playerAch || playerAch.isCompleted) return;

    const achievementData = state.legendaryAchievements.find((la) => la.id === achievementId);
    if (!achievementData) return;

    set((prevState) => ({
      prestigeLevel: prevState.prestigeLevel + achievementData.ppValue,
      playerAchievements: prevState.playerAchievements.map((pa) =>
        pa.achievementId === achievementId
          ? { ...pa, isCompleted: true, completedTimestamp: Date.now() }
          : pa
      ),
    }));
  },

  initiatePrestigeReset: (talentId: string) => {
    const state = get();
    if (state.unlockedLegacyTalents.length >= 15) {
      return { success: false, message: 'Prestige cap reached.' };
    }

    const talent = state.legacyTalents.find((t) => t.id === talentId);
    if (!talent) {
      return { success: false, message: `Legacy Talent not found.` };
    }

    if (state.unlockedLegacyTalents.includes(talentId)) {
      return { success: false, message: `Legacy Talent is already unlocked.` };
    }

    if (state.prestigeLevel < talent.cost) {
      return { success: false, message: `Insufficient PP. Requires ${talent.cost}.` };
    }

    set((prevState) => ({
      prestigeLevel: prevState.prestigeLevel - talent.cost,
      characterLevel: 1,
      skillPoints: 0,
      unlockedLegacyTalents: [...prevState.unlockedLegacyTalents, talentId],
      playerAchievements: prevState.playerAchievements.map((pa) => ({ ...pa, isCompleted: false, completedTimestamp: null })),
    }));

    return { success: true, message: `Rebirth complete! "${talent.name}" unlocked.` };
  },
}));
