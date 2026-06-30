import { CommandDefinitionGUCAv5 } from '@essence/codex';
import { DispatchResult } from '@essence/types';

/**
 * CommandHandler type definition.
 * Returns null if the commandId is not handled by this handler.
 */
export type CommandHandler = (
    commandId: string, 
    params: Record<string, unknown>
) => Promise<DispatchResult | null>;

// Local registry of handlers
const handlers: CommandHandler[] = [];

/**
 * Registers a new command handler with the dispatcher.
 * Handlers are executed in order of registration.
 */
export const registerCommandHandler = (handler: CommandHandler) => {
    handlers.push(handler);
};

/**
 * The central engine for executing GUCA commands.
 * This function translates system-wide directives into executable logic,
 * maintaining the bridge between intent and action.
 *
 * Refactored v3.0 [OMEGA]: Abstracted registration pattern to enforce Star-Chart gravity.
 */
export const dispatchCommand = async (
    command: CommandDefinitionGUCAv5,
    params: Record<string, unknown>,
): Promise<DispatchResult> => {
    try {
        // Iterate through registered handlers
        for (const handler of handlers) {
            const result = await handler(command.commandId, params);
            if (result) return result;
        }

        return {
            success: false,
            message: `The directive '${command.commandId}' is not recognized by any registered system handler.`,
        };
    } catch (error) {
        const errorMsg = error instanceof Error ? error.message : 'Unknown execution failure';
        return { success: false, message: `Execution Anomaly: ${errorMsg}` };
    }
};


