/*
artifact_anchor:
  id: CORE.CELESTIALCHARTVIEW.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/

import * as fs from "node:fs";
import * as path from "node:path";
import * as vscode from "vscode";

export class CelestialChartViewProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = "axion.celestialChart";

  private _view?: vscode.WebviewView;

  constructor(private readonly _extensionUri: vscode.Uri) {}

  public resolveWebviewView(
    webviewView: vscode.WebviewView,
    context: vscode.WebviewViewResolveContext,
    _token: vscode.CancellationToken,
  ) {
    this._view = webviewView;

    webviewView.webview.options = {
      // Allow scripts in the webview
      enableScripts: true,

      localResourceRoots: [this._extensionUri],
    };

    webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

    webviewView.webview.onDidReceiveMessage((data) => {
      switch (data.type) {
        case "achievementClaimed": {
          vscode.commands.executeCommand("axion.claimAchievement", data.id);
          break;
        }
        case "investStardust": {
          vscode.commands.executeCommand("axion.spendStardustInteractive", data.stat, data.amount);
          break;
        }
      }
    });
  }

  public updateStatus(data: any) {
    if (this._view) {
      this._view.webview.postMessage({ type: "updateStatus", data });
    }
  }

  private _getHtmlForWebview(webview: vscode.Webview) {
    // Assets from @fabric layer
    const scriptUri = webview.asWebviewUri(
      vscode.Uri.joinPath(
        this._extensionUri,
        "src",
        "03_fabric",
        "FABR.CelestialChart.LOGIC.js",
      ),
    );
    const styleMainUri = webview.asWebviewUri(
      vscode.Uri.joinPath(
        this._extensionUri,
        "src",
        "03_fabric",
        "FABR.CelestialChart.STYLE.css",
      ),
    );

    // Legacy VSCode styles (optional to move later)
    const styleResetUri = webview.asWebviewUri(
      vscode.Uri.joinPath(this._extensionUri, "media", "reset.css"),
    );
    const styleVSCodeUri = webview.asWebviewUri(
      vscode.Uri.joinPath(this._extensionUri, "media", "vscode.css"),
    );

    const nonce = getNonce();

    const htmlPath = path.join(
      this._extensionUri.fsPath,
      "src",
      "03_fabric",
      "FABR.CelestialChart.UI.html",
    );
    let htmlContent = fs.readFileSync(htmlPath, "utf8");

    htmlContent = htmlContent
      .replace(/\${cspSource}/g, webview.cspSource)
      .replace(/\${nonce}/g, nonce)
      .replace(/\${styleResetUri}/g, styleResetUri.toString())
      .replace(/\${styleVSCodeUri}/g, styleVSCodeUri.toString())
      .replace(/\${styleMainUri}/g, styleMainUri.toString())
      .replace(/\${scriptUri}/g, scriptUri.toString());

    return htmlContent;
  }
}

function getNonce() {
  let text = "";
  const possible =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  for (let i = 0; i < 32; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}
