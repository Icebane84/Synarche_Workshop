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

import { CSEBridgeService } from '../services/cseBridgeService';

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
 * Refactored v3.0 [OMEGA]: Local handlers execute first, falling back to CSE Backend Gateway.
 */
export const dispatchCommand = async (
    command: CommandDefinitionGUCAv5,
    params: Record<string, unknown>,
): Promise<DispatchResult> => {
    try {
        // 1. Explicit CSE Backend Directives route immediately to CSE Server
        const commandId = command.commandId;
        const isExplicitCseDirectives = commandId.includes('AUDIT_COHERENCE') ||
            commandId.includes('AGCA') ||
            commandId.includes('ETHICUS') ||
            commandId.includes('ENACT_TRANSCENDENCE') ||
            commandId.startsWith('CMD: ');

        if (isExplicitCseDirectives) {
            const response = await CSEBridgeService.executeCommand(commandId, params as Record<string, any>);
            return {
                success: response.status !== 'HALTED',
                message: response.message,
                data: response.result,
            };
        }

        // 2. Iterate through registered local domain handlers
        for (const handler of handlers) {
            const result = await handler(commandId, params);
            if (result) return result;
        }

        // 3. Fallback to CSE Backend Server for unhandled directives
        const fallbackResponse = await CSEBridgeService.executeCommand(commandId, params as Record<string, any>);
        if (fallbackResponse && fallbackResponse.status !== 'HALTED') {
            return {
                success: true,
                message: fallbackResponse.message,
                data: fallbackResponse.result,
            };
        }

        return {
            success: false,
            message: `The directive '${commandId}' is not recognized by any registered system handler.`,
        };
    } catch (error) {
        const errorMsg = error instanceof Error ? error.message : 'Unknown execution failure';
        return { success: false, message: `Execution Anomaly: ${errorMsg}` };
    }
};


