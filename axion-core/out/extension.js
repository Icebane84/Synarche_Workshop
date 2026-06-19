"use strict";
/*
artifact_anchor:
  id: CORE.EXTENSION.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/
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
require("./register-paths");
const node_child_process_1 = require("node:child_process");
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const vscode = __importStar(require("vscode"));
const PhoenixSuperpositionEngine_1 = require("./nexus/PhoenixSuperpositionEngine");
const WebClientStrategy_1 = require("./nexus/WebClientStrategy");
const CelestialChartView_1 = require("./CelestialChartView");
const schemas_1 = require("./constants/schemas");
const validation_1 = require("./utils/validation");
/**
 * Activates the Axion Core extension.
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    // Initialize standard strategies for the Phoenix Superposition Engine FSM
    PhoenixSuperpositionEngine_1.PhoenixSuperpositionEngine.registerStrategy("WEB", WebClientStrategy_1.WebClientStrategy);
    context.subscriptions.push(vscode.commands.registerCommand("axion.traverseSpine", handleTraverseSpine), vscode.commands.registerCommand("axion.reforgeArtifact", handleReforgeArtifact), vscode.commands.registerCommand("axion.executePRG", handleExecutePrg), vscode.commands.registerCommand("axion.pushToForge", handlePushToForge), vscode.commands.registerCommand("axion.traceCausality", handleTraceCausality), vscode.commands.registerCommand("axion.verifyTruth", handleVerifyTruth), vscode.commands.registerCommand("axion.consultOracle", handleConsultOracle), vscode.commands.registerCommand("axion.sentinelScan", handleSentinelScan), vscode.commands.registerCommand("axion.claimAchievement", handleClaimAchievement), vscode.commands.registerCommand("axion.checkLevelStatus", handleCheckLevelStatus), vscode.commands.registerCommand("axion.runBackgroundTask", handleRunBackgroundTask), vscode.commands.registerCommand("axion.generateBriefing", handleGenerateBriefing), vscode.commands.registerCommand("axion.viewAuditLog", handleViewAuditLog), vscode.commands.registerCommand("axion.lookupLore", handleLookupLore), vscode.commands.registerCommand("axion.ingestMindMap", handleIngestMindMap), vscode.commands.registerCommand("axion.verifyRegistry", handleVerifyRegistry), vscode.commands.registerCommand("axion.spendStardust", handleSpendStardust), vscode.commands.registerCommand("axion.spendStardustInteractive", async (stat, amount) => {
        executePythonCli(["SPEND_STARDUST", `--target:${stat}`, `--amount:${amount}`, "--json"], (res) => {
            if (res?.success) {
                void vscode.window.showInformationMessage(`Successfully invested ${amount} Stardust into ${stat}!`);
                void vscode.commands.executeCommand("axion.refreshUI");
            }
            else {
                void vscode.window.showErrorMessage(`Upgrade failed: ${res?.error || "Unknown error"}`);
            }
        });
    }), vscode.commands.registerCommand("axion.refreshUI", () => {
        refreshData();
    }));
    const provider = new CelestialChartView_1.CelestialChartViewProvider(context.extensionUri);
    context.subscriptions.push(vscode.window.registerWebviewViewProvider(CelestialChartView_1.CelestialChartViewProvider.viewType, provider));
    // Background refresh for UI
    const refreshData = () => {
        executePythonCli(["get_player_state", "--json"], (state) => {
            if (state && !state.error) {
                const xp = state.xp || 0;
                const level = state.level || 1;
                const nextLevelXp = level * 1000;
                const progress = Math.min(100, Math.max(0, (xp / nextLevelXp) * 100));
                provider.updateStatus({
                    stardust: state.stardust_available,
                    rank: state.prestige_class,
                    progress: progress,
                    achievements: state.achievements || [],
                    stats: {
                        // biome-ignore lint/style/useNamingConvention: database keys
                        coherence_index: state.coherence_index || 1,
                        synergy: state.synergy || 1,
                        adaptability: state.adaptability || 1,
                        transparency: state.transparency || 1,
                    },
                });
            }
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
        executePythonCli(["traverse_spine", artifactId]);
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
        void vscode.window.showInformationMessage(`Reforging ${target} to ${to}...`);
        executePythonCli(["reforge", `--target=${target}`]);
    }
}
async function handleExecutePrg() {
    const target = await vscode.window.showInputBox({
        prompt: "Target Context or Artifact ID",
    });
    const level = await vscode.window.showQuickPick(["STANDARD", "DEEP"], {
        placeHolder: "Select Genesis Level",
    });
    if (target && level) {
        void vscode.window.showInformationMessage(`Initiating ${level} Phoenix Genesis Cycle...`);
        executePythonCli(["genesis", target, level]);
    }
}
async function handlePushToForge() {
    const artifactId = await vscode.window.showInputBox({
        prompt: "Artifact ID to PUSH",
    });
    if (artifactId) {
        void vscode.window.showInformationMessage(`Synchronizing ${artifactId} with Tarot Forge...`);
        executePythonCli(["push", artifactId]);
    }
}
async function handleTraceCausality() {
    const claim = await vscode.window.showInputBox({
        prompt: "Enter logical claim to trace",
    });
    if (claim) {
        void vscode.window.showInformationMessage(`Tracing causality for: ${claim}`);
        executePythonCli(["trace_causality", `--claim="${claim}"`]);
    }
}
async function handleVerifyTruth() {
    const statement = await vscode.window.showInputBox({
        prompt: "Enter statement to verify",
    });
    if (statement) {
        executePythonCli(["verify_truth", `--statement="${statement}"`]);
    }
}
async function handleConsultOracle() {
    const topic = await vscode.window.showInputBox({
        prompt: "Consult Sophia on topic",
    });
    if (topic) {
        executePythonCli(["consult_oracle", `--topic="${topic}"`]);
    }
}
async function handleSentinelScan() {
    const target = await vscode.window.showInputBox({
        prompt: "Target directory or file",
        value: ".",
    });
    if (target) {
        // Calling INITIATE_COMPLIANCE_AUDIT via CLI
        executePythonCli(["INITIATE_COMPLIANCE_AUDIT", `--target="${target}"`]);
    }
}
async function handleClaimAchievement(id) {
    const claimId = id ||
        (await vscode.window.showInputBox({
            prompt: "Enter Milestone ID (e.g. PAM-005)",
        }));
    if (claimId) {
        if (!id) {
            void vscode.window.showInformationMessage(`Claiming achievement: ${claimId}...`);
        }
        executePythonCli(["claim_achievement", `--id=${claimId}`, "--json"], (res) => {
            if (res.success) {
                void vscode.window.showInformationMessage(`Achievement Unlocked: ${claimId}! +${res.stardust_awarded} Stardust.`);
                void vscode.commands.executeCommand("axion.refreshUI");
            }
            else {
                void vscode.window.showErrorMessage(`Failed to claim: ${res.error}`);
            }
        });
    }
}
async function handleCheckLevelStatus() {
    executePythonCli(["check_level_status", "STATUS"]);
}
async function handleSpendStardust() {
    const stats = ["coherence_index", "synergy", "adaptability", "transparency"];
    const stat = await vscode.window.showQuickPick(stats, {
        placeHolder: "Select stat to upgrade",
    });
    const amount = await vscode.window.showInputBox({
        prompt: "Enter Stardust amount to invest (100 = +0.1 boost)",
        value: "100",
        validateInput: (text) => (Number.isNaN(Number(text)) ? "Must be a number" : null),
    });
    if (stat && amount) {
        void vscode.commands.executeCommand("axion.spendStardustInteractive", stat, Number(amount));
    }
}
async function handleRunBackgroundTask() {
    const task = await vscode.window.showInputBox({
        prompt: "Describe background task",
    });
    if (task) {
        executePythonCli(["run_background_task", `--task="${task}"`]);
    }
}
async function handleGenerateBriefing() {
    executePythonCli(["generate_briefing", "NOW"]);
}
// --- New Handlers (Workspace Features) ---
async function handleViewAuditLog() {
    executePythonCli(["ViewAuditLog", "--limit:5"]);
}
async function handleLookupLore() {
    const query = await vscode.window.showInputBox({
        prompt: "Enter query for Lore Search",
    });
    if (query) {
        executePythonCli(["QUERY_LORE", `"${query}"`]);
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
    if (fileUri?.[0]) {
        void vscode.window.showInformationMessage(`Ingesting Mind Map: ${fileUri[0].fsPath}`);
        // Wrap path in quotes to handle spaces
        executePythonCli(["ingest_mindmap", `"${fileUri[0].fsPath}"`]);
    }
}
async function handleVerifyRegistry() {
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0].uri.fsPath;
    if (!workspaceRoot) {
        void vscode.window.showErrorMessage("No active workspace found.");
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
        void vscode.window.showInformationMessage("Registry Validation Successful: Zero Entropy Detected.");
    }
    catch (error) {
        const err = error;
        channel.appendLine(`[Dissonance Detected]: ${err.message}`);
        void vscode.window.showErrorMessage(`Registry Validation Failed: ${err.message}`);
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
    const defaultEnvPath = String.raw `C:\DevEnvironments\master_env\Scripts\python.exe`;
    if (fs.existsSync(defaultEnvPath)) {
        return defaultEnvPath;
    }
    // 6. Fallback
    return "python";
}
function findJsonBounds(str) {
    let start = -1;
    for (let i = 0; i < str.length; i++) {
        if (str[i] === "{" || str[i] === "[") {
            start = i;
            break;
        }
    }
    let end = -1;
    for (let i = str.length - 1; i >= 0; i--) {
        if (str[i] === "}" || str[i] === "]") {
            end = i;
            break;
        }
    }
    return [start, end];
}
function parseCandidateJsons(str, start, end) {
    const candidates = [];
    for (let i = start; i <= end; i++) {
        if (str[i] === "{" || str[i] === "[") {
            candidates.push(str.substring(i, end + 1));
        }
    }
    for (const candidate of candidates) {
        try {
            return JSON.parse(candidate);
        }
        catch {
            // Try next candidate
        }
    }
    return null;
}
function parseCliOutput(stdout) {
    const trimmed = stdout.trim();
    try {
        return JSON.parse(trimmed);
    }
    catch {
        // Ignore and search for substring candidates
    }
    const [startIdx, endIdx] = findJsonBounds(stdout);
    if (startIdx !== -1 && endIdx !== -1 && endIdx > startIdx) {
        return parseCandidateJsons(stdout, startIdx, endIdx);
    }
    return null;
}
/**
 * Executes the centralized Python CLI and returns the output.
 */
function executePythonCli(args, callback) {
    const pythonPath = getPythonExecutablePath();
    const workspaceRoot = path.resolve(__dirname, "..");
    const logicDir = path.join(workspaceRoot, "src", "logic");
    const cliPath = path.join(logicDir, "cli.py");
    const command = `"${pythonPath}" "${cliPath}" ${args.join(" ")}`;
    (0, node_child_process_1.exec)(command, (error, stdout, _stderr) => {
        if (error) {
            console.error(`[Axion] CLI Error: ${error.message}`);
        }
        if (stdout && callback) {
            const parsed = parseCliOutput(stdout);
            if (parsed !== null) {
                callback(parsed);
            }
        }
    });
}
function deactivate() {
    // No specific cleanup required.
}
//# sourceMappingURL=extension.js.map