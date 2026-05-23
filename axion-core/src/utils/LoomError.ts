/**
 * Specific error codes recognized by the Noetic Immune System (NIM).
 * Expanding this list provides granular tracking for telemetry and logging.
 */
/**
 * artifact_anchor:
 * - id:
 * - type:
 */
export type LoomErrorCode =
    | "NIM_VALIDATION_FAILED"
    | "INVALID_STATE_DETECTED"
    | "UNAUTHORIZED_ACCESS"
    | "STRATEGY_RESOLUTION_FAILED"
    | "RATE_LIMIT_EXCEEDED"
    | "NETWORK_FAILURE"
    | "UNKNOWN_ERROR";

/**
 * The standardized error class for the Cognitive Loom.
 * Acts as the ultimate enforcer of the Noetic Immune System.
 */
export class LoomError extends Error {
    public readonly code: LoomErrorCode;
    public readonly statusCode: number;
    public readonly isOperational: boolean;
    public readonly originalError?: unknown;

    constructor(
        message: string,
        code: LoomErrorCode = "UNKNOWN_ERROR",
        statusCode: number = 500,
        isOperational: boolean = true,
        originalError?: unknown,
    ) {
        super(message);
        this.name = "LoomError";
        this.code = code;
        this.statusCode = statusCode;
        this.isOperational = isOperational; // True if expected/handled, False if fatal crash
        this.originalError = originalError;

        // Captures a clean stack trace (V8/Node.js specific)
        if ("captureStackTrace" in Error) {
            (Error as any).captureStackTrace(this, this.constructor);
        }
    }

    /**
     * Factory method to safely convert any unknown error into a standardized LoomError.
     * This is used in catch blocks to normalize raw engine/V8 exceptions.
     */
    public static from(error: unknown): LoomError {
        if (error && typeof error === "object" && (error as any).name === "LoomError") {
            return error as LoomError; // Already standardized, pass it through
        }

        const message = error instanceof Error ? error.message : String(error);
        return new LoomError(message, "UNKNOWN_ERROR", 500, false, error);
    }
}
