import { CommandDefinitionGUCAv5 } from '@essence/codex';

/**
 * @fileoverview Commands for system state, help, and connectivity.
 */

export const systemRecalibrationCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_SYSTEM_RECALIBRATION',
    description: 'Initiates a comprehensive system recalibration.',
    parameters: [],
    action: 'Maintenance cycle.',
    aliases: ['recalibrate', 'optimize', 'reset', 'refresh'],
};

export const getSystemStateCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_GET_SYSTEM_STATE',
    description: 'Retrieves a real-time snapshot of the system Biometrics, Coherence Index, and Active Focus.',
    parameters: [],
    action: 'Snapshot of current core metrics.',
    aliases: ['system state', 'biometrics', 'how are you', 'stats', 'system status'],
};

export const systemHelpCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_SYSTEM_HELP',
    description: 'Displays the command catalog.',
    parameters: [],
    action: 'Help lookup.',
    aliases: ['help', '?', 'commands'],
};

export const deepDiagnosticCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_DEEP_DIAGNOSTIC',
    description: 'Performs a comprehensive audit of system connectivity and substrate health.',
    parameters: [],
    action: 'Deep diagnostic.',
    aliases: ['check connection', 'diagnostic', 'why offline'],
};

export const connectLocalFsCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_CONNECT_LOCAL_FS',
    description: 'Initiates a Neural Link with the local file system.',
    parameters: [],
    action: 'Establish read-write handle.',
    aliases: ['connect', 'link', 'open folder'],
};

export const seedCodebaseGraphCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_SEED_CODEBASE_GRAPH',
    description: 'Maps the project file structure and seeds it as a 3D graph in the Memory Palace.',
    parameters: [],
    action: 'Codebase architecture scan.',
    aliases: ['seed-graph', 'map-codebase', 'index-files'],
};
