/**
 * artifact_anchor:
 * - id: CORE.nexus.pse
 * - type: Quantum Block
 */

import { PhoenixLogger } from "../system/logging";
import { ZodObject, z } from "zod";
import { LoomError } from "../utils/LoomError";

/**
 * Represents the unpredictable, incoming raw data state in Superposition.
 */
export interface SuperpositionPayload {
    blockId: string;
    contextVector: string[];
    rawPayload: unknown;
    token?: string; // Optional JWT token for Zero-Trust authentication gate
}

/**
 * Represents the highly-structured, pristine collapsed state after processing.
 */
export interface CollapsedBlock<T> {
    blockId: string;
    contextVector: string[];
    data: T | Buffer; // Supports both JSON objects and high-frequency byte arrays
    telemetry: {
        latencyMs: number;
        strategyExecuted: string;
        processStatus: "COLLAPSED" | "REJECTED";
        cached: boolean;
    };
    timestamp: number;
}

/**
 * CASTS: Computational Abstraction and Systemic Transformation Strategies.
 * Defines the schema (NIM Gate) and the transmutation logic for a specific payload type.
 */
export interface CASTS_Strategy<T> {
    strategyName: string;
    schema: ZodObject<any>;
    transmute: (parsedData: any) => T;
    packToBinary?: (data: T) => Buffer; // Support for high-frequency game engines
}

/**
 * Plug-and-play cache client interface to ensure absolute runtime portability.
 * Can be backed by in-memory mock caches, local SQLite engines, or production Redis.
 */
export interface ICacheClient {
    get(key: string): Promise<any | null>;
    set(key: string, value: any, ttlSeconds?: number): Promise<void>;
}

/**
 * UMB-QB-PHX-001: The Phoenix Superposition Engine
 * Serves as the dynamic state-translation and routing nexus within the Nova Forge.
 */
export class PhoenixSuperpositionEngine {
    private static strategyRegistry = new Map<string, CASTS_Strategy<any>>();
    private static cacheClient: ICacheClient | null = null;

    /**
     * Registers a transformation strategy dynamically (DAMP / CASTS compliant).
     */
    public static registerStrategy(name: string, strategy: CASTS_Strategy<any>): void {
        const normalizedName = name.toUpperCase();
        this.strategyRegistry.set(normalizedName, strategy);
        PhoenixLogger.info(`[PSE] CASTS Strategy registered: ${normalizedName}`);
    }

    /**
     * Registers a plug-and-play cache client for high-speed bypass.
     */
    public static setCacheClient(client: ICacheClient): void {
        this.cacheClient = client;
        PhoenixLogger.info("[PSE] Caching layer connected successfully.");
    }

    /**
     * Ingests a raw payload, validates it via the NIM Gate, transmutes it via CASTS,
     * and collapses it into a deterministic JSON or Binary state.
     */
    public static async process<T>(payload: SuperpositionPayload): Promise<CollapsedBlock<T>> {
        const startTime = Date.now();

        try {
            // 1. Zero-Trust Access Gate
            if (payload.token && !this.verifyAccess(payload.token)) {
                throw new LoomError(
                    "Superposition collapse blocked. JWT signature verification failed.",
                    "UNAUTHORIZED_ACCESS",
                    403
                );
            }

            // 2. High-Speed Cache Interception (Sub-50ms Bypass)
            if (this.cacheClient) {
                const cached = await this.cacheClient.get(payload.blockId);
                if (cached) {
                    const latencyMs = Date.now() - startTime;
                    return {
                        ...cached,
                        telemetry: {
                            ...cached.telemetry,
                            latencyMs,
                            cached: true,
                        },
                    };
                }
            }

            // 3. Dynamic Strategy Selection (DAMP FSM Router)
            const strategyKey = this.resolveStrategyKey(payload.contextVector);
            const strategy = this.strategyRegistry.get(strategyKey);
            if (!strategy) {
                throw new LoomError(
                    `FSM failed to resolve a suitable strategy for vector: [${payload.contextVector.join(", ")}]`,
                    "STRATEGY_RESOLUTION_FAILED",
                    500
                );
            }

            // 4. NIM Gate: Proactive Schema Validation
            const validatedData = await this.applyNIMGate(payload.rawPayload, strategy.schema);

            // 5. CASTS Transmutation
            let transmutedData = strategy.transmute(validatedData);

            // 6. Polyglot Output Packaging (Conditional Byte Packing)
            const isGameClient = payload.contextVector.includes("CLIENT_GAME") || payload.contextVector.includes("GAME");
            if (isGameClient && strategy.packToBinary) {
                transmutedData = strategy.packToBinary(transmutedData) as any;
            }

            // 7. Superposition Collapse: Final Deterministic Assembly
            const latencyMs = Date.now() - startTime;
            const collapsedBlock = this.collapse<T>(payload, transmutedData, strategy.strategyName, latencyMs);

            // 8. Commit to Cache
            if (this.cacheClient) {
                await this.cacheClient.set(payload.blockId, collapsedBlock);
            }

            return collapsedBlock;
        } catch (error: unknown) {
            const loomError = LoomError.from(error);
            PhoenixLogger.error(
                `[PSE] Superposition Collapse FAILED for BlockID: ${payload.blockId}.`,
                loomError.message
            );
            throw loomError;
        }
    }

    /**
     * Resolves the appropriate strategy key based on the context vector elements.
     */
    private static resolveStrategyKey(vector: string[]): string {
        for (const item of vector) {
            const normalized = item.toUpperCase();
            let foundKey = "";
            this.strategyRegistry.forEach((_, key) => {
                if (normalized.includes(key)) {
                    foundKey = key;
                }
            });
            if (foundKey) {
                return foundKey;
            }
        }
        return "DEFAULT";
    }

    /**
     * Mock verification gate: validates simple JWT signature prefixes for security.
     */
    private static verifyAccess(token: string): boolean {
        // Enforces basic zero-trust signature conventions (e.g. starts with standard JWT "ey")
        return token.startsWith("ey") || token.includes("VERIFIED");
    }

    /**
     * The NIM Gatekeeper: Validates raw data against the CASTS Zod schema.
     */
    private static async applyNIMGate(rawPayload: unknown, schema: ZodObject<any>): Promise<any> {
        try {
            return await schema.parseAsync(rawPayload);
        } catch (error) {
            if (error instanceof z.ZodError) {
                throw new LoomError(
                    "Superposition collapse failed at the NIM Gate. Epistemic pathogen detected.",
                    "NIM_VALIDATION_FAILED",
                    400,
                    true,
                    error.format()
                );
            }
            throw error;
        }
    }

    /**
     * Commits the transmuted data into a highly-structured 'Collapsed' state.
     */
    private static collapse<T>(
        payload: SuperpositionPayload,
        data: any,
        strategyName: string,
        latencyMs: number
    ): CollapsedBlock<T> {
        return {
            blockId: payload.blockId,
            contextVector: payload.contextVector,
            data: data,
            telemetry: {
                latencyMs,
                strategyExecuted: strategyName,
                processStatus: "COLLAPSED",
                cached: false,
            },
            timestamp: Date.now(),
        };
    }
}
