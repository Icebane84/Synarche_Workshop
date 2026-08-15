import { z } from 'zod';

export const LegendaryAchievementSchema = z.object({
	id: z.string(),
	name: z.string(),
	description: z.string(),
	ppValue: z.number().int().positive(), // Prestige Points
});

export const LegacyTalentSchema = z.object({
	id: z.string(),
	name: z.string(),
	description: z.string(),
	cost: z.number().int().positive(), // Prestige Point cost
	tier: z.string(),
});

export const PlayerAchievementSchema = z.object({
	achievementId: z.string(),
	isCompleted: z.boolean(),
	completedTimestamp: z.number().nullable(),
});

export const CognitiveCoreStateSchema = z.object({
	prestigeLevel: z.number().int().nonnegative(),
	characterLevel: z.number().int().positive(),
	skillPoints: z.number().int().nonnegative(),
	legendaryAchievements: z.array(LegendaryAchievementSchema),
	legacyTalents: z.array(LegacyTalentSchema),
	playerAchievements: z.array(PlayerAchievementSchema),
	unlockedLegacyTalents: z.array(z.string()),
});
