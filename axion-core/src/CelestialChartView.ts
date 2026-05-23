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

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource} 'unsafe-inline'; script-src 'nonce-${nonce}';">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="${styleResetUri}" rel="stylesheet">
    <link href="${styleVSCodeUri}" rel="stylesheet">
    <link href="${styleMainUri}" rel="stylesheet">
    <title>Celestial Chart</title>
</head>
<body>
    <div class="liquid-glass-container">
        <header>
            <h1 class="glow-text">AXION CELESTIAL HUB</h1>
            <div class="prestige-badge">
                <span id="prestige-rank">INITIATE</span>
                <div class="progress-bar-container">
                    <div id="prestige-progress" class="progress-bar" style="width: 30%"></div>
                </div>
            </div>
        </header>

        <section class="stardust-display">
            <div class="stardust-icon">✦</div>
            <div class="stardust-value" id="stardust-count">0</div>
            <div class="stardust-label">COGNITIVE SYNERGY</div>
        </section>

        <nav class="chart-navigation">
            <button class="nav-item active" data-view="achievements">CANONS</button>
            <button class="nav-item" data-view="skills">AXIOMS</button>
            <button class="nav-item" data-view="lore">CODEX</button>
        </nav>

        <main id="view-content">
            <div class="achievement-list" id="achievement-list">
                <div class="achievement-item locked">
                    <div class="achievement-info">
                        <div class="achievement-name">COHERENCE_INIT</div>
                        <div class="achievement-desc">Loading system integrity parameters...</div>
                    </div>
                </div>
            </div>
        </main>

        <footer>
            <div class="sync-status">
                <span class="status-dot green"></span>
                <span class="status-text">COHERENCE: 100% [OMEGA]</span>
            </div>
        </footer>
    </div>

    <script nonce="${nonce}" src="${scriptUri}"></script>
</body>
</html>`;
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
