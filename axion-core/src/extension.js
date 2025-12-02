const vscode = require("vscode");

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  console.log('Congratulations, your extension "axion-core" is now active!');

  let disposable = vscode.commands.registerCommand(
    "axion.helloWorld",
    function () {
      vscode.window.showInformationMessage("Hello World from Axion Core!");
    },
  );

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
};
