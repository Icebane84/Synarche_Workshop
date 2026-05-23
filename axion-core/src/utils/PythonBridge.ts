/**
 * artifact_anchor:
 * - id:
 * - type:
 */
import { spawn } from "child_process";
import path from "path";
import { PhoenixLogger } from "../system/logging";

export class PythonBridge {
    /**
     * Polyglot Weaving: Spawns a Python process, pipes data via stdin, and parses stdout.
     */
    public static async execute<T>(scriptName: string, data: unknown): Promise<T> {
        return new Promise((resolve, reject) => {
            // Resolve the path assuming scripts live in a standard python or scripts directory
            const scriptPath = path.resolve(process.cwd(), "src/cse", scriptName);

            PhoenixLogger.info(`[PolyglotWeaving] Invoking script: ${scriptName}`);

            // 1. Point directly to your master environment's executable
            // Allow an environment variable override for deployment flexibility
            const pythonExecutable = process.env.PYTHON_PATH || "C:\\DevEnvironments\\master_env\\Scripts\\python.exe";

            const pyProcess = spawn(pythonExecutable, [scriptPath]);
            let outputData = "";
            let errorData = "";

            // Send the perfectly formatted, safely validated JSON to Python
            pyProcess.stdin.write(JSON.stringify(data));
            pyProcess.stdin.end();

            pyProcess.stdout.on("data", (chunk) => {
                outputData += chunk.toString();
            });
            pyProcess.stderr.on("data", (chunk) => {
                errorData += chunk.toString();
            });

            pyProcess.on("close", (code) => {
                if (code !== 0) {
                    PhoenixLogger.error(`[PolyglotWeaving] Python exit code ${code}. Error: ${errorData}`);
                    return reject(new Error(`Python Execution Failed: ${errorData}`));
                }

                try {
                    resolve(JSON.parse(outputData) as T);
                } catch (parseError) {
                    PhoenixLogger.error(`[PolyglotWeaving] Failed to parse Python output. Raw: ${outputData}`);
                    reject(new Error("Failed to parse Polyglot Weaving output"));
                }
            });
        });
    }
}
