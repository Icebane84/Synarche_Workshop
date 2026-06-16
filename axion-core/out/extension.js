"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const node_child_process_1 = require("node:child_process");
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const vscode = __importStar(require("vscode"));
const schemas_1 = require("./constants/schemas");
const validation_1 = require("./utils/validation");
const CelestialChartView_1 = require("./CelestialChartView");
const PhoenixSuperpositionEngine_1 = require("./nexus/PhoenixSuperpositionEngine");
const WebClientStrategy_1 = require("./nexus/WebClientStrategy");
/**
 * Activates the Axion Core extension.
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    // Initialize standard strategies for the Phoenix Superposition Engine FSM
    PhoenixSuperpositionEngine_1.PhoenixSuperpositionEngine.registerStrategy("WEB", WebClientStrategy_1.WebClientStrategy);
    context.subscriptions.push(vscode.commands.registerCommand("axion.traverseSpine", handleTraverseSpine), vscode.commands.registerCommand("axion.reforgeArtifact", handleReforgeArtifact), vscode.commands.registerCommand("axion.executePRG", handleExecutePRG), vscode.commands.registerCommand("axion.pushToForge", handlePushToForge), vscode.commands.registerCommand("axion.traceCausality", handleTraceCausality), vscode.commands.registerCommand("axion.verifyTruth", handleVerifyTruth), vscode.commands.registerCommand("axion.consultOracle", handleConsultOracle), vscode.commands.registerCommand("axion.sentinelScan", handleSentinelScan), vscode.commands.registerCommand("axion.claimAchievement", handleClaimAchievement), vscode.commands.registerCommand("axion.checkLevelStatus", handleCheckLevelStatus), vscode.commands.registerCommand("axion.runBackgroundTask", handleRunBackgroundTask), vscode.commands.registerCommand("axion.generateBriefing", handleGenerateBriefing), vscode.commands.registerCommand("axion.viewAuditLog", handleViewAuditLog), vscode.commands.registerCommand("axion.lookupLore", handleLookupLore), vscode.commands.registerCommand("axion.ingestMindMap", handleIngestMindMap), vscode.commands.registerCommand("axion.verifyRegistry", handleVerifyRegistry), vscode.commands.registerCommand("axion.spendStardust", handleSpendStardust));
    const provider = new CelestialChartView_1.CelestialChartViewProvider(context.extensionUri);
    context.subscriptions.push(vscode.window.registerWebviewViewProvider(CelestialChartView_1.CelestialChartViewProvider.viewType, provider));
    // Background refresh for UI
    const refreshData = () => {
        executePythonCLI(["get_player_state", "--json"], (state) => {
            executePythonCLI(["get_achievements", "--json"], (achievements) => {
                provider.updateStatus({
                    stardust: state.stardust,
                    rank: state.rank,
                    progress: state.xp_progress,
                    achievements: achievements,
                });
            });
        });
    };
    setInterval(refreshData, 30000); // Every 30 seconds
    refreshData(); // Initial load
}
// --- Command Handlers ---
async function handleTraverseSpine() {
    const artifactId = await vscode.window.showInputBox({
        prompt: 'Enter Artifact ID to start traversal (e.g. UMB-CSE-001) or "list"',
        placeHolder: "UMB-OSLM-001",
    });
    if (artifactId) {
        executePythonCLI(["traverse_spine", artifactId]);
    }
}
async function handleReforgeArtifact() {
    const target = await vscode.window.showInputBox({
        prompt: "Target Artifact ID or Path",
    });
    const to = await vscode.window.showQuickPick(["v10.0", "UMB-OSLM"], {
        placeHolder: "Target Format",
    });
    if (target && to) {
        vscode.window.showInformationMessage(`Reforging ${target} to ${to}...`);
        executePythonCLI(["reforge", "--target=" + target]);
    }
}
async function handleExecutePRG() {
    const target = await vscode.window.showInputBox({
        prompt: "Target Context or Artifact ID",
    });
    const level = await vscode.window.showQuickPick(["STANDARD", "DEEP"], {
        placeHolder: "Select Genesis Level",
    });
    if (target && level) {
        vscode.window.showInformationMessage(`Initiating ${level} Phoenix Genesis Cycle...`);
        executePythonCLI(["genesis", target, level]);
    }
}
async function handlePushToForge() {
    const artifactId = await vscode.window.showInputBox({
        prompt: "Artifact ID to PUSH",
    });
    if (artifactId) {
        vscode.window.showInformationMessage(`Synchronizing ${artifactId} with Tarot Forge...`);
        executePythonCLI(["push", artifactId]);
    }
}
async function handleTraceCausality() {
    const claim = await vscode.window.showInputBox({
        prompt: "Enter logical claim to trace",
    });
    if (claim) {
        vscode.window.showInformationMessage(`Tracing causality for: ${claim}`);
        executePythonCLI(["trace_causality", `--claim="${claim}"`]);
    }
}
async function handleVerifyTruth() {
    const statement = await vscode.window.showInputBox({
        prompt: "Enter statement to verify",
    });
    if (statement) {
        executePythonCLI(["verify_truth", `--statement="${statement}"`]);
    }
}
async function handleConsultOracle() {
    const topic = await vscode.window.showInputBox({
        prompt: "Consult Sophia on topic",
    });
    if (topic) {
        executePythonCLI(["consult_oracle", `--topic="${topic}"`]);
    }
}
async function handleSentinelScan() {
    const target = await vscode.window.showInputBox({
        prompt: "Target directory or file",
        value: ".",
    });
    if (target) {
        // Calling INITIATE_COMPLIANCE_AUDIT via CLI
        executePythonCLI(["INITIATE_COMPLIANCE_AUDIT", `--target="${target}"`]);
    }
}
async function handleClaimAchievement(id) {
    const claimId = id ||
        (await vscode.window.showInputBox({
            prompt: "Enter Milestone ID (e.g. PAM-005)",
        }));
    if (claimId) {
        if (!id) {
            vscode.window.showInformationMessage(`Claiming achievement: ${claimId}...`);
        }
        executePythonCLI(["claim_achievement", `--id=${claimId}`, "--json"], (res) => {
            if (res.success) {
                vscode.window.showInformationMessage(`Achievement Unlocked: ${claimId}! +${res.stardust_awarded} Stardust.`);
                // Trigger global refresh (if we can access the refreshData function,
                // or just wait for the interval. For now, let's just trigger it manually if we were to expose it).
                // Since refreshData is inside activate, we'd need to refactor.
            }
            else {
                vscode.window.showErrorMessage(`Failed to claim: ${res.error}`);
            }
        });
    }
}
async function handleCheckLevelStatus() {
    executePythonCLI(["check_level_status", "STATUS"]);
}
async function handleSpendStardust() {
    const stats = ["coherence_index", "synergy", "adaptability", "transparency"];
    const stat = await vscode.window.showQuickPick(stats, {
        placeHolder: "Select stat to upgrade",
    });
    const amount = await vscode.window.showInputBox({
        prompt: "Enter Stardust amount to invest (100 = +0.1 boost)",
        value: "100",
        validateInput: (text) => (isNaN(Number(text)) ? "Must be a number" : null),
    });
    if (stat && amount) {
        vscode.window.showInformationMessage(`Investing ${amount} Stardust in ${stat}...`);
        executePythonCLI(["SPEND_STARDUST", stat, amount]);
    }
}
async function handleRunBackgroundTask() {
    const task = await vscode.window.showInputBox({
        prompt: "Describe background task",
    });
    if (task) {
        executePythonCLI(["run_background_task", `--task="${task}"`]);
    }
}
async function handleGenerateBriefing() {
    executePythonCLI(["generate_briefing", "NOW"]);
}
// --- New Handlers (Workspace Features) ---
async function handleViewAuditLog() {
    executePythonCLI(["ViewAuditLog", "--limit:5"]);
}
async function handleLookupLore() {
    const query = await vscode.window.showInputBox({
        prompt: "Enter query for Lore Search",
    });
    if (query) {
        executePythonCLI(["QUERY_LORE", `"${query}"`]);
    }
}
async function handleIngestMindMap() {
    const options = {
        canSelectMany: false,
        openLabel: "Ingest Map",
        filters: {
            "Freeplane Maps": ["mm"],
            "All Files": ["*"],
        },
    };
    const fileUri = await vscode.window.showOpenDialog(options);
    if (fileUri && fileUri[0]) {
        vscode.window.showInformationMessage(`Ingesting Mind Map: ${fileUri[0].fsPath}`);
        // Wrap path in quotes to handle spaces
        executePythonCLI(["ingest_mindmap", `"${fileUri[0].fsPath}"`]);
    }
}
async function handleVerifyRegistry() {
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0].uri.fsPath;
    if (!workspaceRoot) {
        vscode.window.showErrorMessage("No active workspace found.");
        return;
    }
    const registryPath = path.join(workspaceRoot, "axion-core", "assets", "PRS-001.json");
    const channel = vscode.window.createOutputChannel("Axion [Registry]");
    channel.show(true);
    try {
        if (!fs.existsSync(registryPath)) {
            throw new Error(`Registry not found at: ${registryPath}`);
        }
        channel.appendLine(`[VIGIL] Starting validation of: ${registryPath}`);
        const data = JSON.parse(fs.readFileSync(registryPath, "utf8"));
        (0, validation_1.validateMetadata)(data, schemas_1.PRS_001_SCHEMA);
        channel.appendLine("[SUCCESS] Registry structural integrity verified.");
        vscode.window.showInformationMessage("Registry Validation Successful: Zero Entropy Detected.");
    }
    catch (error) {
        channel.appendLine(`[Dissonance Detected]: ${error.message}`);
        vscode.window.showErrorMessage(`Registry Validation Failed: ${error.message}`);
    }
}
// --- Helper Functions ---
/**
 * Resolves the path to the Python executable based on settings, environment variables,
 * and standard defaults.
 */
function getPythonExecutablePath() {
    // 1. Check workspace settings for "axion.pythonPath"
    const axionConfig = vscode.workspace.getConfiguration("axion");
    const axionPath = axionConfig.get("pythonPath");
    if (axionPath && fs.existsSync(axionPath)) {
        return axionPath;
    }
    // 2. Check workspace settings for "python.defaultInterpreterPath"
    const pythonConfig = vscode.workspace.getConfiguration("python");
    const defaultPath = pythonConfig.get("defaultInterpreterPath");
    if (defaultPath && fs.existsSync(defaultPath)) {
        return defaultPath;
    }
    // 3. Check legacy "python.pythonPath"
    const legacyPath = pythonConfig.get("pythonPath");
    if (legacyPath && fs.existsSync(legacyPath)) {
        return legacyPath;
    }
    // 4. Check environment variable
    if (process.env.PYTHON_PATH && fs.existsSync(process.env.PYTHON_PATH)) {
        return process.env.PYTHON_PATH;
    }
    // 5. Check master environment default on Windows
    const defaultEnvPath = "C:\\DevEnvironments\\master_env\\Scripts\\python.exe";
    if (fs.existsSync(defaultEnvPath)) {
        return defaultEnvPath;
    }
    // 6. Fallback
    return "python";
}
/**
 * Executes the centralized Python CLI and returns the output.
 */
function executePythonCLI(args, callback) {
    const pythonPath = getPythonExecutablePath();
    const workspaceRoot = path.resolve(__dirname, "..");
    const logicDir = path.join(workspaceRoot, "src", "logic");
    const cliPath = path.join(logicDir, "cli.py");
    const command = `"${pythonPath}" "${cliPath}" ${args.join(" ")}`;
    const channel = vscode.window.createOutputChannel("Axion [Core]");
    // channel.show(true); // Don't pop up for every background call
    (0, node_child_process_1.exec)(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`[Axion] CLI Error: ${error.message}`);
        }
        if (stdout && callback) {
            try {
                const json = JSON.parse(stdout);
                callback(json);
            }
            catch (e) {
                // Not JSON, ignore for callback
            }
        }
    });
}
function deactivate() {
    // No specific cleanup required.
}
//# sourceMappingURL=extension.js.map