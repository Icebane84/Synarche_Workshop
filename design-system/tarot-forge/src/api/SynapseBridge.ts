import type { CommandDefinitionGUCAv5, DispatchResult } from '../types/synapseTypes';
import { BridgeClient } from './BridgeClient';

// Initial registry with a basic command for testing
export const commandRegistry: Record<string, CommandDefinitionGUCAv5> = {
    CMD_STATUS: {
        commandId: 'CMD_STATUS',
        description: 'Check the status of the Synarche Bridge connection.',
        action: 'status',
        parameters: [],
        aliases: ['status', 'check connection'],
    },
    CMD_OPEN_VSCODE: {
        commandId: 'CMD_OPEN_VSCODE',
        description: 'Open VS Code to a specific path.',
        action: 'open_vscode',
        parameters: [{ name: 'path', type: 'string', description: 'Path to open', required: true }],
        aliases: ['code', 'open'],
    },
};

export const dispatchCommand = async (
    command: CommandDefinitionGUCAv5,
    params: Record<string, any>
): Promise<DispatchResult> => {
    console.log(`[SynapseBridge] Dispatching ${command.commandId} with params:`, params);

    // Convert to BridgeClient format (command + args)
    // Currently BridgeClient.cast takes a string command like "open_vscode C:/path"
    // We need to construct this string if we want to use the current BridgeClient logic,
    // OR we update BridgeClient to handle structured objects.
    // For now, let's just pass the raw commandId and params to the bridge if we expand it,
    // but looking at BridgeClient.ts, it sends { command: "..." } to the server.
    // The server executes 'Synarche <command>'.

    try {
        // Construct the CLI-like argument string
        let argsString = '';
        if (params) {
            Object.values(params).forEach((val) => {
                argsString += ` "${val}"`;
            });
        }

        // Use the 'action' field from GUCA as the command keyword
        const commandString = `${command.action}${argsString}`;

        const response = await BridgeClient.cast(commandString);

        return {
            success: true, // If cast throws, we catch below.
            message: `Executed: ${response || 'Command sent successfully.'}`,
            data: { raw: response },
        };
    } catch (err) {
        return {
            success: false,
            message: err instanceof Error ? err.message : 'Unknown bridge error',
        };
    }
};

export const interpretNaturalLanguageCommand = async (query: string): Promise<string | null> => {
    // Simple mock implementation for now
    // In a real implementation, this would call an LLM or use fuzzy matching
    const lowerQuery = query.toLowerCase();

    if (lowerQuery.includes('status') || lowerQuery.includes('check')) {
        return 'CMD_STATUS';
    }

    return null;
};

// Helper for resonance/echo (mocked for now)
export const getResonantCommands = (commands: CommandDefinitionGUCAv5[], limit: number = 3) => {
    return commands.slice(0, limit);
};

export const getEchoCommands = (_location: string, _focus: string) => {
    return [];
};

export const trackCommandExecution = (id: string) => {
    console.log(`[Metric] Executed ${id}`);
};
