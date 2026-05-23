/**
 * artifact_anchor:
 * - id:
 * - type:
 */
import * as assert from "assert";
import { CollapsedBlock } from "@nexus/PhoenixSuperpositionEngine";
import { PythonBridge } from "@utils/PythonBridge";

suite("Integration Test: Python Polyglot Weaving", () => {
    test("should successfully pipe data to cse.py and receive JSON response", async () => {
        // 1. Arrange: Create a mock CollapsedBlock
        const mockBlock: CollapsedBlock<{ command: string }> = {
            blockId: "integration-test-999",
            contextVector: ["TEST_ENV"],
            data: { command: "INIT_TEST" },
            telemetry: {
                latencyMs: 10,
                strategyExecuted: "TEST_STRATEGY",
                processStatus: "COLLAPSED",
                cached: false,
            },
            timestamp: Date.now(),
        };

        // 2. Act: Execute the bridge (This spawns the actual python process)
        const result = await PythonBridge.execute<any>("cse.py", mockBlock);

        // 3. Assert: Validate the Python script correctly received and processed the data
        assert.strictEqual(result.status, "SYNTHESIZED", "Python script did not return expected status");
        assert.strictEqual(result.processedData.command, "INIT_TEST", "Data payload was corrupted during transit");
    });

    test("should reject the promise if Python exits with an error code", async () => {
        // Send malformed data to force a crash in a hypothetical script or unhandled scenario
        try {
            // Pointing to a script that doesn't exist to force an error state
            await PythonBridge.execute<any>("non_existent_script.py", {});
            assert.fail("Execution should have thrown an error");
        } catch (error) {
            assert.ok(error instanceof Error);
            assert.ok(error.message.includes("Python Execution Failed") || error.message.includes("ENOENT"));
        }
    });
});
