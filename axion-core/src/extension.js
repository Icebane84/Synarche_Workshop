const vscode = require("vscode");
const { exec } = require("child_process");
const path = require("path");

/**
 * Safely resolves the Synarche Workspace root.
 */
function getSynarcheWorkspaceRoot() {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders || workspaceFolders.length === 0) {
        vscode.window.showErrorMessage("No workspace is open. Please open your 'Synarche_Workspace' folder.");
        return null;
    }
    const rootFolder =
        workspaceFolders.find((folder) => folder.name.toLowerCase() === "synarche_workspace") || workspaceFolders[0];
    return rootFolder.uri.fsPath;
}

/**
 * A universal executor that automatically sets the CWD for all child processes.
 */
function execWorkspaceCommand(fullCommand) {
    const workspaceRoot = getSynarcheWorkspaceRoot();
    if (!workspaceRoot) {
        return Promise.reject("Workspace root not found.");
    }

    return new Promise((resolve, reject) => {
        exec(fullCommand, { cwd: workspaceRoot }, (error, stdout, stderr) => {
            if (error) {
                reject(stderr || error.message);
            } else {
                resolve(stdout);
            }
        });
    });
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log("Axion Core extension is now active in the Synarche Workspace.");

    // Example command implementation for 'axion.reforgeArtifact' from your package.json
    let reforgeCommand = vscode.commands.registerCommand("axion.reforgeArtifact", () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showInformationMessage("Cannot reforge: No active text editor.");
            return;
        }

        const workspaceRoot = getSynarcheWorkspaceRoot();
        if (!workspaceRoot) {
            return; // Error message is shown in the helper function
        }

        const targetFile = editor.document.uri.fsPath;

        // 1. Construct absolute paths to your Python tools
        const reforgerScriptPath = path.join(workspaceRoot, "axion-core", "tools", "reforge.py");

        // 2. Define options for the child process, CRUCIALLY setting the CWD
        const options = {
            // Set the Current Working Directory. Python scripts can now use relative paths from here.
            cwd: workspaceRoot,
        };

        const command = `python "${reforgerScriptPath}" --target "${targetFile}"`;

        vscode.window.showInformationMessage(`Axion is executing: ${command}`);

        exec(command, options, (error, stdout, stderr) => {
            if (error) {
                console.error(`Reforge Error: ${error.message}`);
                vscode.window.showErrorMessage(`Reforge Failed: ${stderr || "Check the debug console."}`);
                return;
            }
            console.log(`Reforge Output: ${stdout}`);
            vscode.window.showInformationMessage(`Artifact '${path.basename(targetFile)}' reforged successfully.`);
        });
    });

    context.subscriptions.push(reforgeCommand);

    // Refactored helper using the new unified workspace command runner
    const execCliCommand = (command, args = []) => {
        const pythonPath = "python"; // Assume python is in PATH or configured
        const cliPath = path.join(context.extensionPath, "src", "cli.py");
        const fullCommand = `${pythonPath} "${cliPath}" ${command} ${args.join(" ")}`;

        // Automatically applies cwd: workspaceRoot
        return execWorkspaceCommand(fullCommand);
    };

    // Command: Hello World
    let helloWorld = vscode.commands.registerCommand("axion.helloWorld", () => {
        vscode.window.showInformationMessage("Hello World from Axion Core!");
    });

    // Command: Audit Compliance
    let auditCompliance = vscode.commands.registerCommand("axion.auditCompliance", async () => {
        const activeEditor = vscode.window.activeTextEditor;
        if (!activeEditor) {
            vscode.window.showErrorMessage("No active editor found.");
            return;
        }

        const filePath = activeEditor.document.fileName;
        if (!filePath.endsWith(".md")) {
            vscode.window.showWarningMessage("Compliance Audit only supports Markdown files.");
            return;
        }

        vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: "Axion: Running Compliance Audit...",
                cancellable: false,
            },
            async () => {
                try {
                    const result = await execCliCommand("INITIATE_COMPLIANCE_AUDIT", [`--target:"${filePath}"`]);
                    vscode.window.showInformationMessage(`Audit Complete: ${result}`);
                    // TODO: Parse results and show in a more structured way (e.g. Problems view)
                } catch (err) {
                    vscode.window.showErrorMessage(`Audit Failed: ${err}`);
                }
            },
        );
    });

    // Command: Lookup Lore
    let lookupLore = vscode.commands.registerCommand("axion.lookupLore", async () => {
        const query = await vscode.window.showInputBox({
            prompt: "Enter your lore query (e.g. 'The Phoenix Protocol')",
            placeHolder: "Search the knowledge base...",
        });

        if (!query) return;

        vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: "Axion: Searching Knowledge Base...",
                cancellable: false,
            },
            async () => {
                try {
                    const result = await execCliCommand("QUERY_LORE", [`"${query}"`]);
                    // Show result in a webview or output channel
                    const channel = vscode.window.createOutputChannel("Axion: Lore");
                    channel.appendLine(`--- Lore Search Result for: ${query} ---`);
                    channel.appendLine(result);
                    channel.show();
                } catch (err) {
                    vscode.window.showErrorMessage(`Lore Search Failed: ${err}`);
                }
            },
        );
    });

    // Command: View Audit Log
    let viewAuditLog = vscode.commands.registerCommand("axion.viewAuditLog", async () => {
        vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: "Axion: Fetching Audit Log...",
                cancellable: false,
            },
            async () => {
                try {
                    const result = await execCliCommand("ViewAuditLog", ["--limit:10"]);
                    const channel = vscode.window.createOutputChannel("Axion: Audit Log");
                    channel.clear();
                    channel.appendLine(result);
                    channel.show();
                } catch (err) {
                    vscode.window.showErrorMessage(`Failed to view log: ${err}`);
                }
            },
        );
    });

    context.subscriptions.push(helloWorld, auditCompliance, lookupLore, viewAuditLog);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate,
};
