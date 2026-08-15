import { z } from 'zod';

/**
 * Zod schema for a legendary achievement.
 * These are one-time, high-impact goals.
 */
export const LegendaryAchievementSchema = z.object({
	id: z.string().uuid(),
	name: z.string(),
	description: z.string(),
	ppValue: z.number().int().positive(), // Prestige Points
});

/**
 * Zod schema for a legacy talent.
 * These are permanent, account-wide unlocks.
 */
export const LegacyTalentSchema = z.object({
	id: z.string().uuid(),
	name: z.string(),
	description: z.string(),
	cost: z.number().int().positive(), // Prestige Point cost
	tier: z.string(), // Could be an enum if tiers are well-defined
});

/**
 * Zod schema for tracking a player's achievement status.
 */
export const PlayerAchievementSchema = z.object({
	achievementId: z.string().uuid(),
	isCompleted: z.boolean(),
	completedTimestamp: z.number().nullable(),
});

/**
 * Zod schema for the entire state of the Cognitive Core store.
 * This defines the shape and types of all state variables.
 */
export const CognitiveCoreStateSchema = z.object({
	prestigeLevel: z.number().int().nonnegative(),
	characterLevel: z.number().int().positive(),
	skillPoints: z.number().int().nonnegative(),
	legendaryAchievements: z.array(LegendaryAchievementSchema),
	legacyTalents: z.array(LegacyTalentSchema),
	playerAchievements: z.array(PlayerAchievementSchema),
	unlockedLegacyTalents: z.array(z.string().uuid()),
});