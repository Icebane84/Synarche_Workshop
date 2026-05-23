/**
 * artifact_anchor:
 * - id: CORE.nexus.redis_cache
 * - type: Cache Client
 */

import { ICacheClient } from "./PhoenixSuperpositionEngine";
import { PhoenixLogger } from "@logging";
import Redis from "ioredis";

/**
 * Standard states for the State-Based Circuit Breaker.
 */
export enum BreakerState {
    CLOSED = "CLOSED",         // Normal operations: queries Redis
    OPEN = "OPEN",             // Redis is down: instantly bypasses query to avoid latency
    HALF_OPEN = "HALF_OPEN"    // Cooldown expired: tests a single query to check Redis health
}

/**
 * Resilient, fault-tolerant Redis cache client equipped with a State-Based Circuit Breaker.
 * Conforms to UMB-QB-PHX-001 by preserving absolute high-availability and zero-blockage execution.
 */
export class RedisCacheClient implements ICacheClient {
    private redis: Redis;
    private state: BreakerState = BreakerState.CLOSED;
    private failureCount: number = 0;
    private lastStateChange: number = Date.now();
    private cooldownPeriodMs: number = 30000; // 30-second cooldown period

    constructor(connectionString: string) {
        // Initialize Redis with short connection timeouts to prevent system hang
        this.redis = new Redis(connectionString, {
            maxRetriesPerRequest: 1,
            connectTimeout: 2000, // 2-second connection timeout
            lazyConnect: true // Prevent throwing on instantiation if Redis is offline
        });

        this.redis.on("error", (err) => {
            PhoenixLogger.warning(`[PSE Cache Connection Warning] Redis connection issue: ${err.message}`);
        });
    }

    /**
     * Attempts a high-speed GET query. 
     * Bypasses immediately if the Circuit Breaker is active.
     */
    public async get(key: string): Promise<any | null> {
        if (this.isBreakerOpenAndActive()) {
            // Instant Cache Miss Bypass (Sub-microsecond, zero network latency)
            return null;
        }

        try {
            const data = await this.redis.get(key);
            this.recordSuccess();

            if (!data) return null;
            return JSON.parse(data);
        } catch (error: any) {
            this.recordFailure(error);
            return null; // Graceful soft fallback
        }
    }

    /**
     * Attempts a high-speed SET query with TTL.
     * Bypasses immediately if the Circuit Breaker is active.
     */
    public async set(key: string, value: any, ttlSeconds: number = 300): Promise<void> {
        if (this.isBreakerOpenAndActive()) {
            return;
        }

        try {
            const serialized = JSON.stringify(value);
            await this.redis.set(key, serialized, "EX", ttlSeconds);
            this.recordSuccess();
        } catch (error: any) {
            this.recordFailure(error);
        }
    }

    /**
     * Gracefully disconnects the Redis connection on system shutdown.
     */
    public async disconnect(): Promise<void> {
        try {
            await this.redis.quit();
            PhoenixLogger.info("[PSE] Redis cache connection quit cleanly.");
        } catch (err) {
            this.redis.disconnect();
        }
    }

    /**
     * Public visibility helper to retrieve current breaker state.
     */
    public getBreakerState(): BreakerState {
        return this.state;
    }

    /**
     * Public visibility helper to retrieve current failure count.
     */
    public getFailureCount(): number {
        return this.failureCount;
    }

    /**
     * Checks if the Circuit Breaker is active and blocking queries.
     * Integrates automatic cooldown-to-half-open transitions.
     */
    private isBreakerOpenAndActive(): boolean {
        if (this.state === BreakerState.OPEN) {
            const timePassed = Date.now() - this.lastStateChange;
            if (timePassed > this.cooldownPeriodMs) {
                this.state = BreakerState.HALF_OPEN;
                this.lastStateChange = Date.now();
                PhoenixLogger.warning("[PSE Cache Breaker] Cooldown expired. Entering HALF-OPEN state to test Redis.");
                return false; // Allow a test query to flow through
            }
            return true; // Breaker is active; block and bypass
        }
        return false; // Breaker is CLOSED or HALF-OPEN; let queries flow
    }

    /**
     * Tracks successful queries, restoring the CLOSED state if in HALF-OPEN.
     */
    private recordSuccess(): void {
        if (this.state === BreakerState.HALF_OPEN) {
            this.state = BreakerState.CLOSED;
            this.failureCount = 0;
            this.lastStateChange = Date.now();
            PhoenixLogger.info("[PSE Cache Breaker] Redis connection restored. Re-entering CLOSED state (Normal Operations).");
        } else if (this.state === BreakerState.CLOSED) {
            this.failureCount = 0; // Reset flaky count on success
        }
    }

    /**
     * Tracks query failures. Trips the breaker to OPEN after 3 consecutive failures.
     */
    private recordFailure(error: any): void {
        PhoenixLogger.warning(`[PSE Cache Warning] Cache query failed: ${error.message}`);
        this.handleError(error);
    }

    /**
     * Enforces the FSM state changes for connection/query errors.
     */
    private handleError(error: any): void {
        if (this.state === BreakerState.CLOSED) {
            this.failureCount++;
            if (this.failureCount >= 3) {
                this.state = BreakerState.OPEN;
                this.lastStateChange = Date.now();
                PhoenixLogger.critical(
                    `[PSE Cache Breaker] 3 consecutive failures encountered. TRIPPING BREAKER to OPEN. Bypassing Redis cache for next ${this.cooldownPeriodMs / 1000} seconds.`
                );
            }
        } else if (this.state === BreakerState.HALF_OPEN) {
            this.state = BreakerState.OPEN;
            this.lastStateChange = Date.now();
            PhoenixLogger.critical(
                `[PSE Cache Breaker] Test query failed in HALF-OPEN. Re-entering OPEN state. Bypassing Redis cache for next ${this.cooldownPeriodMs / 1000} seconds.`
            );
        }
    }
}
