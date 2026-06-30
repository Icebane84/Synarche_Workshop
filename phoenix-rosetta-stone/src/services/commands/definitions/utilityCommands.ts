import { CommandDefinitionGUCAv5 } from '@essence/codex';

/**
 * @fileoverview Utility commands for raw file operations and directives.
 */

export const beginClcCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_BEGIN_CLC',
    description: 'Begin a new Cognitive Language Construction.',
    parameters: [],
    action: 'Switch to CLC mode.',
    aliases: ['clc', 'macro', 'chain'],
};

export const executeDirectiveCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_EXECUTE_DIRECTIVE',
    description: 'Executes a natural language directive.',
    parameters: [
        { name: 'instruction', type: 'string', description: 'Instruction text.', required: true, uiHint: 'textarea' },
    ],
    action: 'Directive execution.',
    aliases: ['do', 'run', 'exec', 'execute'],
};

export const initiateAutoRepairCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_INITIATE_AUTO_REPAIR',
    description: 'Deploys autonomous repair agents.',
    parameters: [],
    action: 'Auto-repair.',
    aliases: ['repair', 'fix', 'patch'],
};

export const applyFixCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_APPLY_FIX',
    description: 'Applies a cognitive fix or patch to a local source file via the Neural Link.',
    parameters: [
        {
            name: 'filePath',
            type: 'string',
            description: 'Relative path (e.g., "components/Header.tsx").',
            required: true,
        },
        {
            name: 'patchContent',
            type: 'string',
            description: 'The new source content.',
            required: true,
            uiHint: 'textarea',
        },
    ],
    action: 'Code Smith patching.',
    aliases: ['fix file', 'patch code', 'apply patch', 'write code'],
};

export const readFileCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_READ_FILE',
    description: 'Reads the content of a local file via the Neural Link.',
    parameters: [
        { name: 'filePath', type: 'string', description: 'Relative path (e.g., "src/App.tsx").', required: true },
    ],
    action: 'File read.',
    aliases: ['read file', 'cat', 'open file', 'read'],
};

export const syncSkillSeltCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_SYNC_SKILL_SELT',
    description: 'Synchronizes Gold Standard experience logs from the database to a specific skill\'s SELT.md.',
    parameters: [
        {
            name: 'skillName',
            type: 'string',
            description: 'The name of the skill folder (e.g., "plan-writing").',
            required: true,
        },
        {
            name: 'minCoherence',
            type: 'number',
            description: 'Filter for Gold Standard (default 0.8).',
            required: false,
        },
    ],
    action: 'Experience harvesting.',
    aliases: ['sync selt', 'harvest logs', 'skill sync'],
};
