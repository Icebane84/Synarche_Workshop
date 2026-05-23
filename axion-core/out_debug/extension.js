"use strict";
var __createBinding =
  (this && this.__createBinding) ||
  (Object.create
    ? function (o, m, k, k2) {
        if (k2 === undefined) k2 = k;
        var desc = Object.getOwnPropertyDescriptor(m, k);
        if (
          !desc ||
          ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)
        ) {
          desc = {
            enumerable: true,
            get: function () {
              return m[k];
            },
          };
        }
        Object.defineProperty(o, k2, desc);
      }
    : function (o, m, k, k2) {
        if (k2 === undefined) k2 = k;
        o[k2] = m[k];
      });
var __setModuleDefault =
  (this && this.__setModuleDefault) ||
  (Object.create
    ? function (o, v) {
        Object.defineProperty(o, "default", { enumerable: true, value: v });
      }
    : function (o, v) {
        o["default"] = v;
      });
var __importStar =
  (this && this.__importStar) ||
  (function () {
    var ownKeys = function (o) {
      ownKeys =
        Object.getOwnPropertyNames ||
        function (o) {
          var ar = [];
          for (var k in o)
            if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
          return ar;
        };
      return ownKeys(o);
    };
    return function (mod) {
      if (mod && mod.__esModule) return mod;
      var result = {};
      if (mod != null)
        for (var k = ownKeys(mod), i = 0; i < k.length; i++)
          if (k[i] !== "default") __createBinding(result, mod, k[i]);
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
/**
 * Activates the Axion Core extension.
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand("axion.traverseSpine", handleTraverseSpine),
    vscode.commands.registerCommand(
      "axion.reforgeArtifact",
      handleReforgeArtifact,
    ),
    vscode.commands.registerCommand("axion.executePRG", handleExecutePRG),
    vscode.commands.registerCommand("axion.pushToForge", handlePushToForge),
    vscode.commands.registerCommand(
      "axion.traceCausality",
      handleTraceCausality,
    ),
    vscode.commands.registerCommand("axion.verifyTruth", handleVerifyTruth),
    vscode.commands.registerCommand("axion.consultOracle", handleConsultOracle),
    vscode.commands.registerCommand("axion.sentinelScan", handleSentinelScan),
    vscode.commands.registerCommand(
      "axion.claimAchievement",
      handleClaimAchievement,
    ),
    vscode.commands.registerCommand(
      "axion.checkLevelStatus",
      handleCheckLevelStatus,
    ),
    vscode.commands.registerCommand(
      "axion.runBackgroundTask",
      handleRunBackgroundTask,
    ),
    vscode.commands.registerCommand(
      "axion.generateBriefing",
      handleGenerateBriefing,
    ),
    vscode.commands.registerCommand("axion.viewAuditLog", handleViewAuditLog),
    vscode.commands.registerCommand("axion.lookupLore", handleLookupLore),
    vscode.commands.registerCommand("axion.ingestMindMap", handleIngestMindMap),
    vscode.commands.registerCommand(
      "axion.verifyRegistry",
      handleVerifyRegistry,
    ),
  );
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
    vscode.window.showInformationMessage(
      `Initiating ${level} Phoenix Genesis Cycle...`,
    );
    executePythonCLI(["genesis", target, level]);
  }
}
async function handlePushToForge() {
  const artifactId = await vscode.window.showInputBox({
    prompt: "Artifact ID to PUSH",
  });
  if (artifactId) {
    vscode.window.showInformationMessage(
      `Synchronizing ${artifactId} with Tarot Forge...`,
    );
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
async function handleClaimAchievement() {
  const id = await vscode.window.showInputBox({
    prompt: "Enter Milestone ID (e.g. PAM-005)",
  });
  if (id) {
    executePythonCLI(["claim_achievement", `--id=${id}`]);
  }
}
async function handleCheckLevelStatus() {
  executePythonCLI(["check_level_status", "STATUS"]);
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
    vscode.window.showInformationMessage(
      `Ingesting Mind Map: ${fileUri[0].fsPath}`,
    );
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
  const registryPath = path.join(
    workspaceRoot,
    "axion-core",
    "assets",
    "PRS-001.json",
  );
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
    vscode.window.showInformationMessage(
      "Registry Validation Successful: Zero Entropy Detected.",
    );
  } catch (error) {
    channel.appendLine(`[Dissonance Detected]: ${error.message}`);
    vscode.window.showErrorMessage(
      `Registry Validation Failed: ${error.message}`,
    );
  }
}
// --- Helper Functions ---
/**
 * Executes the centralized Python CLI with appropriate arguments.
 */
function executePythonCLI(args) {
  const pythonPath = "python"; // Assumes python is in PATH
  // Corrected Path: cli.py is now in src/logic/cli.py relative to extension.js
  // workspace/
  //   src/
  //     extension.ts  -> out/extension.js
  //     logic/
  //       cli.py
  // When running from out/extension.js:
  // __dirname is .../out
  // We need to go up to root, then src/logic?
  // Wait, tsconfig output is "out". "src/logic/cli.py" is a source file.
  // We should copy src/logic to out/logic OR reference src/logic directly if we are in dev mode.
  // For simplicity, we reference the src path assuming the Workspace is the root.
  // Better: Use workspace root.
  // However, __dirname in a built extension points to dist or out.
  // Let's assume standard structure:
  // root/
  //   out/extension.js
  //   src/logic/cli.py
  const workspaceRoot = path.resolve(__dirname, ".."); // Up from out/
  const logicDir = path.join(workspaceRoot, "src", "logic");
  const cliPath = path.join(logicDir, "cli.py");
  const command = `${pythonPath} "${cliPath}" ${args.join(" ")}`;
  // Create output channel once
  const channel = vscode.window.createOutputChannel("Axion [Core]");
  channel.show(true);
  channel.appendLine(`> Executing: ${command}`);
  (0, node_child_process_1.exec)(command, (error, stdout, stderr) => {
    if (error) {
      channel.appendLine(`[ERROR]: ${error.message}`);
    }
    if (stderr) {
      channel.appendLine(`[STDERR]: ${stderr}`);
    }
    if (stdout) {
      channel.appendLine(stdout);
    }
    channel.appendLine("--- End of Output ---");
  });
}
function deactivate() {
  // No specific cleanup required.
}
//# sourceMappingURL=extension.js.map
