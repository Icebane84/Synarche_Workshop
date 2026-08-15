// [OMEGA AST Cleaned]: Tokenized design standards applied.

import { ExperienceLog } from '@essence/types';
import { dispatchCommand } from '../system/commandDispatcher';
import { syncSkillSeltCommand } from './commands/definitions/utilityCommands';

/**
 * Sovereign Sync Service
 * Coordinates the automated harvesting of Gold Standard experiences.
 */
export const triggerSovereignSync = async (log: ExperienceLog) => {
    // Only trigger if we achieve Gold Standard (OPTIMAL consistency)
    if (log.phenomenologicalState.internalConsistency !== 'OPTIMAL') {
        return;
    }

    // Determine the skill name from the module or intent
    // Defaulting to plan-writing or the module of origin
    const skillName = log.contextualMeta.moduleOfOrigin === 'CognitiveInterface' 
        ? 'plan-writing' // Pilot default
        : log.contextualMeta.moduleOfOrigin.toLowerCase();

    try {
        await dispatchCommand(syncSkillSeltCommand, {
            skillName,
            minCoherence: 0.8
        });
    } catch (error) {
        console.warn('[Sovereign-Sync] Automated sync cycle deferred due to Neural Link state.', error);
    }
};

