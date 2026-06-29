/**
 * Provides a rigid, predictable structure for all system commands (GUCA).
 * This is the engine of our "Codified Language," ensuring every directive
 * is unambiguous and executable.
 */
export interface CommandDefinitionGUCAv5 {
    commandId: string; // e.g., 'CMD_REFACTOR_COMPONENT'
    description: string;
    parameters: {
        name: string;
        type: 'string' | 'number' | 'boolean' | 'string[]';
        description: string;
        required: boolean;
        uiHint?: 'artifact' | 'textarea';
    }[];
    action: string; // Describes the command's function
    /**
     * Optional shorthand triggers or natural language equivalents for this command.
     * Used for rapid lookup and to assist the natural language interpreter.
     */
    aliases?: string[];
}

export interface DispatchResult {
    success: boolean;
    message: string;
    data?: Record<string, unknown>;
}

export interface CoherenceDissonance {
    id: `DISS-${string}`;
    type: string;
    description: string;
    sourceArtifacts: string[];
    severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
    timestamp: number;
}
