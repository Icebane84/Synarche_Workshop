import * as assert from "assert";
import { z } from "zod";
import {
    PhoenixSuperpositionEngine,
    CASTS_Strategy,
    ICacheClient,
    SuperpositionPayload
} from "@nexus/PhoenixSuperpositionEngine";
import { LoomError } from "@utils/LoomError";
import { RedisCacheClient, BreakerState } from "@nexus/RedisCacheClient";

// --- MOCK TRANSFORMATION STRATEGIES ---

interface WebData {
    layout: string;
    theme: "light" | "dark";
    message: string;
}

const WebClientStrategy: CASTS_Strategy<WebData> = {
    strategyName: "WEB_STRATEGY",
    schema: z.object({
        layout: z.string().min(1),
        theme: z.enum(["light", "dark"]),
        message: z.string().default("Welcome, Agent.")
    }) as any,
    transmute: (parsedData: any): WebData => {
        return {
            layout: parsedData.layout.toUpperCase(),
            theme: parsedData.theme,
            message: `${parsedData.message} | System Coherent`
        };
    }
};

interface GameData {
    entityId: string;
    position: { x: number; y: number; z: number };
}

const GameEngineStrategy: CASTS_Strategy<GameData> = {
    strategyName: "GAME_STRATEGY",
    schema: z.object({
        entityId: z.string().uuid(),
        x: z.number(),
        y: z.number(),
        z: z.number().default(0)
    }) as any,
    transmute: (parsedData: any): GameData => {
        return {
            entityId: parsedData.entityId,
            position: { x: parsedData.x, y: parsedData.y, z: parsedData.z }
        };
    },
    packToBinary: (data: GameData): Buffer => {
        const buffer = Buffer.alloc(28);
        buffer.write(data.entityId.replace(/-/g, "").substring(0, 16), 0, "ascii");
        buffer.writeFloatLE(data.position.x, 16);
        buffer.writeFloatLE(data.position.y, 20);
        buffer.writeFloatLE(data.position.z, 24);
        return buffer;
    }
};

class MockInMemoryCache implements ICacheClient {
    private cache = new Map<string, any>();
    public async get(key: string): Promise<any | null> {
        return this.cache.get(key) || null;
    }
    public async set(key: string, value: any, ttlSeconds?: number): Promise<void> {
        this.cache.set(key, value);
    }
}

// --- TEST RUNNER SUITE ---
async function runTests() {
    console.log("==================================================");
    console.log("⚡ STARTING PHOENIX SUPERPOSITION ASSEMBLY AUDIT");
    console.log("==================================================");

    // Initial Registration (Startup phase simulation)
    PhoenixSuperpositionEngine.registerStrategy("WEB", WebClientStrategy);
    PhoenixSuperpositionEngine.registerStrategy("GAME", GameEngineStrategy);

    const mockCache = new MockInMemoryCache();
    PhoenixSuperpositionEngine.setCacheClient(mockCache);

    console.log("\n--------------------------------------------------");
    console.log("🧪 Test Case 1: Web Strategy Ingestion & Collapse (JSON)");
    
    const webPayload: SuperpositionPayload = {
        blockId: "block-web-999",
        contextVector: ["CLIENT_WEB", "AUTH_OK"],
        rawPayload: {
            layout: "dashboard-grid",
            theme: "dark",
            message: "Initiate Genesis Cycle"
        },
        token: "ey-verified-token"
    };

    const collapsedWeb = await PhoenixSuperpositionEngine.process<WebData>(webPayload);
    console.log("Result:", JSON.stringify(collapsedWeb, null, 2));

    assert.strictEqual(collapsedWeb.blockId, "block-web-999");
    assert.strictEqual(collapsedWeb.telemetry.strategyExecuted, "WEB_STRATEGY");
    assert.strictEqual(collapsedWeb.telemetry.processStatus, "COLLAPSED");
    
    const webData = collapsedWeb.data as WebData;
    assert.strictEqual(webData.layout, "DASHBOARD-GRID");
    assert.strictEqual(webData.theme, "dark");
    console.log("🟢 Test Case 1 Passed!");

    console.log("\n--------------------------------------------------");
    console.log("🧪 Test Case 2: High-Speed Cache Interception Check");
    
    const collapsedWebCached = await PhoenixSuperpositionEngine.process<WebData>(webPayload);
    assert.strictEqual(collapsedWebCached.telemetry.cached, true);
    console.log("🟢 Test Case 2 Passed!");

    console.log("\n--------------------------------------------------");
    console.log("🧪 Test Case 3: Game Strategy Ingestion & Binary Packing");

    const gamePayload: SuperpositionPayload = {
        blockId: "block-game-777",
        contextVector: ["CLIENT_GAME", "SYSTEM_DEV"],
        rawPayload: {
            entityId: "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
            x: 150.75,
            y: -75.25,
            z: 10.5
        },
        token: "ey-verified-token"
    };

    const collapsedGame = await PhoenixSuperpositionEngine.process<GameData>(gamePayload);
    assert.ok(Buffer.isBuffer(collapsedGame.data));
    console.log("🟢 Test Case 3 Passed!");

    console.log("\n--------------------------------------------------");
    console.log("🧪 Test Case 4: Zero-Trust Security Block (Invalid JWT)");

    const securePayload: SuperpositionPayload = {
        blockId: "block-secure-888",
        contextVector: ["CLIENT_WEB"],
        rawPayload: { layout: "default", theme: "light" },
        token: "invalid-token-prefix"
    };

    try {
        await PhoenixSuperpositionEngine.process(securePayload);
        assert.fail("Security verification should have failed.");
    } catch (err) {
        assert.strictEqual((err as any).name, "LoomError");
        const loomErr = err as LoomError;
        assert.strictEqual(loomErr.code, "UNAUTHORIZED_ACCESS");
        console.log("🟢 Test Case 4 Passed!");
    }

    console.log("\n--------------------------------------------------");
    console.log("🧪 Test Case 5: NIM Gate Validation Failure (Zod Check)");

    const badDataPayload: SuperpositionPayload = {
        blockId: "block-fail-111",
        contextVector: ["CLIENT_WEB"],
        rawPayload: {
            layout: "",
            theme: "invalid-theme-value"
        },
        token: "ey-verified-token"
    };

    try {
        await PhoenixSuperpositionEngine.process(badDataPayload);
        assert.fail("Schema validation should have blocked bad data.");
    } catch (err) {
        assert.strictEqual((err as any).name, "LoomError");
        assert.strictEqual((err as any).code, "NIM_VALIDATION_FAILED");
        console.log("🟢 Test Case 5 Passed!");
    }

    console.log("\n--------------------------------------------------");
    console.log("🧪 Test Case 6: FSM Strategy Mapping Failure");

    const unmappedPayload: SuperpositionPayload = {
        blockId: "block-unmapped-222",
        contextVector: ["CLIENT_UNSUPPORTED_TYPE"],
        rawPayload: { data: "irrelevant" },
        token: "ey-verified-token"
    };

    try {
        await PhoenixSuperpositionEngine.process(unmappedPayload);
        assert.fail("FSM router should have thrown resolution failure.");
    } catch (err) {
        assert.strictEqual((err as any).name, "LoomError");
        assert.strictEqual((err as any).code, "STRATEGY_RESOLUTION_FAILED");
        console.log("🟢 Test Case 6 Passed!");
    }

    console.log("\n--------------------------------------------------");
    console.log("🧪 Test Case 7: Resilient State-Based Redis Circuit Breaker");

    // Initialize with a port guaranteed to fail (offline address)
    const redisClient = new RedisCacheClient("redis://127.0.0.1:9999");
    PhoenixSuperpositionEngine.setCacheClient(redisClient);

    console.log("[Test Setup] Connected offline Redis. Current Breaker State:", redisClient.getBreakerState());
    assert.strictEqual(redisClient.getBreakerState(), BreakerState.CLOSED);

    // Call 1: Trigger first unprocessed request (Fails GET and SET, failureCount = 2)
    console.log("\n--- Triggering Flaky Query 1 ---");
    const res1 = await PhoenixSuperpositionEngine.process(webPayload);
    assert.strictEqual(res1.telemetry.processStatus, "COLLAPSED"); // Operational fallback succeeds
    assert.strictEqual(redisClient.getFailureCount(), 2);
    assert.strictEqual(redisClient.getBreakerState(), BreakerState.CLOSED);

    // Call 2: Trigger second request (Fails GET, trips failureCount to 3, opening breaker instantly)
    console.log("\n--- Triggering Flaky Query 2 (Tripping) ---");
    await PhoenixSuperpositionEngine.process(webPayload);
    assert.strictEqual(redisClient.getBreakerState(), BreakerState.OPEN);

    // Call 4: Instant Bypass Query
    // Breaker is OPEN. Should instantly bypass Redis without any network connection timeout.
    console.log("\n--- Triggering Instant Bypass Query (Breaker OPEN) ---");
    const bypassStartTime = Date.now();
    const resBypass = await PhoenixSuperpositionEngine.process(webPayload);
    const bypassDuration = Date.now() - bypassStartTime;
    
    console.log(`Bypass query completed in ${bypassDuration}ms.`);
    assert.strictEqual(resBypass.telemetry.processStatus, "COLLAPSED");
    assert.strictEqual(redisClient.getBreakerState(), BreakerState.OPEN);
    assert.ok(bypassDuration < 100, "Bypass query should execute instantly (under 100ms) without waiting for network timeout.");

    await redisClient.disconnect();
    console.log("🟢 Test Case 7 Passed!");

    console.log("\n==================================================");
    console.log("✨ ALL TEST CASES PASSED WITH 100% COHERENCE!");
    console.log("==================================================");
}

runTests().catch(err => {
    console.error("❌ CRITICAL UNHANDLED ERROR IN SUITE:", err);
    if (err && err.originalError) {
        console.error("Original Error Details:", JSON.stringify(err.originalError, null, 2));
    }
    process.exit(1);
});
