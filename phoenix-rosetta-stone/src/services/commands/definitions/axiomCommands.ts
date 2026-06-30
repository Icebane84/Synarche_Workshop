import { CommandDefinitionGUCAv5 } from '@essence/codex';

/**
 * @fileoverview Commands for the Axiom Memory Palace (Supabase).
 */

export const axiomRememberCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_AXIOM_REMEMBER',
    description: 'Crystallizes new knowledge into the Axion Memory Palace (Supabase).',
    parameters: [
        {
            name: 'content',
            type: 'string',
            description: 'The knowledge, insight, or fact to remember.',
            required: true,
            uiHint: 'textarea',
        },
        {
            name: 'domain',
            type: 'string',
            description: 'Knowledge domain (e.g., "Architecture", "UserPreferences", "CodePattern").',
            required: false,
        },
        {
            name: 'layer',
            type: 'number',
            description: 'Memory layer: 2=Kinetic, 3=Semantic, 4=Sovereign (default: 2).',
            required: false,
        },
        {
            name: 'tags',
            type: 'string',
            description: 'Comma-separated tags for retrieval (e.g., "vite,typescript,pattern").',
            required: false,
        },
    ],
    action: 'Memory crystallization.',
    aliases: ['remember', 'memorize', 'store memory', 'recall save', 'learn this'],
};

export const axiomRecallCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_AXIOM_RECALL',
    description: 'Retrieves memories from the Axion Memory Palace by semantic query.',
    parameters: [
        {
            name: 'query',
            type: 'string',
            description: 'What to recall — keywords, topic, or concept.',
            required: true,
        },
        {
            name: 'limit',
            type: 'number',
            description: 'Max memories to return (default: 5).',
            required: false,
        },
        {
            name: 'domain',
            type: 'string',
            description: 'Filter by domain (optional).',
            required: false,
        },
    ],
    action: 'Memory retrieval.',
    aliases: ['recall', 'remember what', 'search memory', 'what do you know about', 'memory search'],
};

export const axiomSynthesizeCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_AXIOM_SYNTHESIZE',
    description: 'Forges a high-value insight as an L1 Sovereign Gem in the Memory Palace.',
    parameters: [
        {
            name: 'content',
            type: 'string',
            description: 'The insight or architectural truth to crystallize as a Gem.',
            required: true,
            uiHint: 'textarea',
        },
        {
            name: 'insight_label',
            type: 'string',
            description: 'Short label for the gem (e.g., "Liquid Glass Pattern").',
            required: true,
        },
        {
            name: 'domain',
            type: 'string',
            description: 'Domain for the gem (default: "SovereignInsight").',
            required: false,
        },
    ],
    action: 'Gem forging.',
    aliases: ['synthesize', 'forge gem', 'gem this', 'crystallize insight', 'make gem'],
};

export const axiomStatusCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_AXIOM_STATUS',
    description: 'Displays Memory Palace health metrics, gem count, and activation statistics.',
    parameters: [],
    action: 'Memory Palace diagnostics.',
    aliases: ['status', 'memory status', 'palace status', 'axiom health', 'memory stats', 'how much do you remember'],
};
