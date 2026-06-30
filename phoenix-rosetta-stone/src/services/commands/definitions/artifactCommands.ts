import { CommandDefinitionGUCAv5 } from '@essence/codex';

/**
 * @fileoverview Commands for artifact interactions and analysis.
 */

export const analyzeSynergyCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_ANALYZE_ARTIFACT_SYNERGY',
    description: 'Analyzes a target artifact for potential synergies.',
    parameters: [
        {
            name: 'artifactId',
            type: 'string',
            description: 'The unique identifier of the artifact.',
            required: true,
            uiHint: 'artifact',
        },
    ],
    action: 'Synergy analysis.',
    aliases: ['analyze', 'synergy', 'inspect'],
};

export const fetchArtifactMetadataCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_FETCH_ARTIFACT_METADATA',
    description: 'Retrieves detailed metadata for a specific system artifact.',
    parameters: [
        {
            name: 'artifactId',
            type: 'string',
            description: 'The unique identifier of the artifact.',
            required: true,
            uiHint: 'artifact',
        },
    ],
    action: 'Metadata look-up.',
    aliases: ['get artifact', 'artifact info', 'lookup artifact'],
};

export const fetchAllArtifactsCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_FETCH_ALL_ARTIFACTS',
    description: 'Retrieves a complete catalog of all system artifacts within the Celestial Chart.',
    parameters: [],
    action: 'Global artifact retrieval.',
    aliases: ['list all artifacts', 'all artifacts', 'catalog', 'show nodes'],
};

export const simulateSynergyCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_SIMULATE_SYNERGY',
    description: 'Simulates synergy between two artifacts with Dream Weave UI.',
    parameters: [
        { name: 'artifactId1', type: 'string', description: 'ID 1', required: true, uiHint: 'artifact' },
        { name: 'artifactId2', type: 'string', description: 'ID 2', required: true, uiHint: 'artifact' },
    ],
    action: 'Predictive simulation.',
    aliases: ['simulate', 'fusion', 'predict'],
};
