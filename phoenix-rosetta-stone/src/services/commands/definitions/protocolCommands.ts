import { CommandDefinitionGUCAv5 } from '@essence/codex';

/**
 * @fileoverview Protocol-level commands for cloud synchronization and handshake.
 */

export const syncProtocolLibraryCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_SYNC_PROTOCOL_LIBRARY',
    description: 'Synchronizes the local Neural Archive with the Sovereign Backend (pgvector).',
    parameters: [
        {
            name: 'overwrite',
            type: 'boolean',
            description: 'Overwrite existing artifacts in the cloud.',
            required: false,
        },
    ],
    action: 'Knowledge base hydration.',
    aliases: ['sync artifacts', 'upload knowledge', 'hydrate backend'],
};

export const invokeCloudFunctionCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_INVOKE_CLOUD_FUNCTION',
    description: 'Invokes a Supabase Edge Function for remote processing.',
    parameters: [
        {
            name: 'functionName',
            type: 'string',
            description: 'Name of the edge function (e.g., "process-storage-file").',
            required: true,
        },
        {
            name: 'body',
            type: 'string',
            description: 'JSON string for the function payload.',
            required: false,
            uiHint: 'textarea',
        },
    ],
    action: 'Edge function invocation.',
    aliases: ['call function', 'edge invoke', 'cloud process'],
};

export const testBackendHandshakeCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_TEST_BACKEND_HANDSHAKE',
    description: 'Verifies Supabase credentials and table accessibility.',
    parameters: [],
    action: 'Handshake verification.',
    aliases: ['test connection', 'ping backend', 'handshake'],
};

export const indexKnowledgeCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_INDEX_KNOWLEDGE',
    description: 'Hydrates the Supabase vector store with local knowledge base.',
    parameters: [],
    action: 'Vector Indexing',
    aliases: ['index', 'upload knowledge', 'seed vector store'],
};

export const migrateTasksCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_MIGRATE_TASKS',
    description: 'Migrates local tasks to the Sovereign Backend (Supabase).',
    parameters: [],
    action: 'Cloud migration.',
    aliases: ['migrate tasks', 'upload tasks', 'sync to cloud'],
};
