const vscode = require("vscode");
const { exec } = require("child_process");
const path = require("path");

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Congratulations, your extension "axion-core" is now active!');

    const execCliCommand = (command, args = []) => {
        const pythonPath = "python"; // Assume python is in PATH or configured
        const cliPath = path.join(context.extensionPath, "src", "cli.py");
        const fullCommand = `${pythonPath} "${cliPath}" ${command} ${args.join(" ")}`;

        return new Promise((resolve, reject) => {
            exec(fullCommand, (error, stdout, stderr) => {
                if (error) {
                    reject(stderr || error.message);
                } else {
                    resolve(stdout);
                }
            });
        });
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
