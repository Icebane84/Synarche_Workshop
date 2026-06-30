import { CommandDefinitionGUCAv5 } from '@essence/codex';

/**
 * @fileoverview Commands for system audits, dissonance scans, and linting.
 */

export const scanForDissonanceCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_SCAN_FOR_DISSONANCE',
    description: 'Scans the system for cognitive dissonances.',
    parameters: [
        { name: 'errorSource', type: 'string', description: 'Error Source', required: false },
        { name: 'errorContext', type: 'string', description: 'Error Context', required: false },
    ],
    action: 'Dissonance audit.',
    aliases: ['scan', 'audit', 'dissonance', 'debug'],
};

export const harmonyScanCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_HARMONY_SCAN',
    description:
        'Performs a deep diagnostic scan of the project to identify prop-drilling and component bloat violations.',
    parameters: [],
    action: 'Deep Harmony Audit.',
    aliases: ['harmony scan', 'check bloat', 'prop drill scan'],
};

export const scanLocalProjectCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_SCAN_LOCAL_PROJECT',
    description: 'Scans the connected local project for protocol violations.',
    parameters: [],
    action: 'AST Audit.',
    aliases: ['scan local', 'check code', 'audit project'],
};

export const runLintCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_RUN_LINT',
    description: 'Executes the project linter to check for style and error violations.',
    parameters: [],
    action: 'Linting check.',
    aliases: ['lint', 'check code', 'run linter', 'verify style'],
};
