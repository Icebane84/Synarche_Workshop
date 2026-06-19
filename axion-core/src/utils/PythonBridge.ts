/*
artifact_anchor:
  id: CORE.PYTHONBRIDGE.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/

/**
 * artifact_anchor:
 * - id:
 * - type:
 */
import { PhoenixLogger } from "@system/logging";
import { spawn } from "node:child_process";
import path from "node:path";

export class PythonBridge {
    /**
     * Polyglot Weaving: Spawns a Python process and parses JSON output.
     */
    public static async execute<T>(scriptName: string, data: unknown): Promise<T> {
        const scriptPath = path.resolve(process.cwd(), "src/cse", scriptName);
        const pythonExecutable = process.env.PYTHON_PATH || String.raw`C:\DevEnvironments\master_env\Scripts\python.exe`;

        PhoenixLogger.info(`[PolyglotWeaving] Invoking script: ${scriptName}`);

        return new Promise((resolve, reject) => {
            const pyProcess = spawn(pythonExecutable, [scriptPath]);
            let outputData = "";
            let errorData = "";

            pyProcess.stdin.write(JSON.stringify(data));
            pyProcess.stdin.end();

            pyProcess.stdout.on("data", (chunk) => { outputData += chunk.toString(); });
            pyProcess.stderr.on("data", (chunk) => { errorData += chunk.toString(); });

            pyProcess.on("close", (code) => {
                if (code !== 0) {
                    PhoenixLogger.error(`[PolyglotWeaving] Python exit code ${code}. Error: ${errorData}`);
                    return reject(new Error(`Python Execution Failed: ${errorData}`));
                }
                try {
                    resolve(this.extractJson<T>(outputData));
                } catch (parseError) {
                    PhoenixLogger.error(`[PolyglotWeaving] Failed to parse Python output. Raw: ${outputData}`);
                    reject(parseError);
                }
            });
        });
    }

    /**
     * Extracts and parses the first valid JSON object or array from a string.
     */
    private static extractJson<T>(input: string): T {
        const text = input.trim();
        // Attempt direct parse first
        try { return JSON.parse(text) as T; } catch { /* continue to extraction */ }

        const startIdx = text.search(/[{\[]/);
        const endIdx = Math.max(text.lastIndexOf("}"), text.lastIndexOf("]"));

        if (startIdx === -1 || endIdx === -1 || endIdx <= startIdx) {
            throw new Error("No valid JSON structure found in output");
        }

        const candidates = this.generateCandidates(text.substring(startIdx, endIdx + 1));
        for (const candidate of candidates) {
            try { return JSON.parse(candidate) as T; } catch { continue; }
        }

        throw new Error("Failed to parse any JSON candidates from output");
    }

    /**
     * Generates potential JSON substrings from a block of text.
     */
    private static generateCandidates(block: string): string[] {
        const candidates: string[] = [];
        for (let i = 0; i < block.length; i++) {
            if (block[i] === "{" || block[i] === "[") {
                candidates.push(block.substring(i));
            }
        }
        return candidates;
    }
}
