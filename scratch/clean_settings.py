import json

# Construct clean settings dictionary
settings = {
    "editor.fontSize": 16,
    "editor.formatOnSave": True,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.semanticHighlighting.enabled": True,
    "editor.guides.bracketPairs": True,
    "editor.renderWhitespace": "selection",
    "editor.minimap.enabled": False,
    "editor.fontLigatures": True,
    "editor.codeActionsOnSave": {
        "source.fixAll": "explicit",
        "source.organizeImports": "explicit",
        "source.fixAll.eslint": "explicit",
        "source.organizeImports.biome": "explicit"
    },
    "editor.rulers": [100],
    "editor.wordWrap": "wordWrapColumn",
    "editor.wordWrapColumn": 100,
    "files.trimTrailingWhitespace": True,
    "files.insertFinalNewline": True,

    "python.defaultInterpreterPath": "C:\\DevEnvironments\\master_env\\Scripts\\python.exe",
    "python.analysis.extraPaths": ["axion-core", "open-notebook"],
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.indexing": False,
    "python.analysis.diagnosticMode": "openFilesOnly",
    "python.analysis.exclude": [
        "**/node_modules",
        "**/__pycache__",
        "**/.git",
        "**/.venv",
        "**/venv",
        "**/_governance",
        "**/.archives",
        "**/.mypy_cache",
        "**/.ruff_cache",
        "**/scratch",
        "**/incoming",
        "**/dist",
        "**/out"
    ],

    "eslint.useFlatConfig": True,
    "eslint.validate": ["javascript", "typescript", "typescriptreact", "markdown"],
    "eslint.workingDirectories": [
        { "directory": "axion-core", "changeProcessCWD": True },
        { "directory": "phoenix-rosetta-stone", "changeProcessCWD": True },
        { "directory": "design-system", "changeProcessCWD": True },
        { "directory": ".", "changeProcessCWD": False },
        { "directory": "open-notebook", "changeProcessCWD": True },
        { "directory": "nova_forge", "changeProcessCWD": True }
    ],
    "eslint.run": "onSave",

    "mypy-type-checker.args": ["--config-file", "./axion-core/standards/mypy.ini"],
    "mypy-type-checker.importStrategy": "fromEnvironment",
    "mypy-type-checker.interpreter": ["C:\\DevEnvironments\\master_env\\Scripts\\python.exe"],
    "mypy-type-checker.path": ["C:\\DevEnvironments\\master_env\\Scripts\\mypy.exe"],
    "mypy.dmypyExecutable": "C:\\DevEnvironments\\master_env\\Scripts\\dmypy.exe",
    "mypy-type-checker.daemonStatusFile": "axion-core\\standards\\.dmypy.json",

    "ruff.interpreter": ["C:\\DevEnvironments\\master_env\\Scripts\\python.exe"],
    "ruff.path": ["C:\\DevEnvironments\\master_env\\Scripts\\ruff.exe"],
    "ruff.importStrategy": "fromEnvironment",

    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
        }
    },
    "[javascript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[typescript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[json]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[jsonc]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[markdown]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2,
        "editor.insertSpaces": True,
        "editor.codeActionsOnSave": {
            "source.fixAll": "never"
        }
    },

    "markdownlint.customRules": [
        "./axion-core/standards/eslint-plugin-phoenix/markdownlint-rules/axion-rules.cjs",
        "./axion-core/standards/eslint-plugin-phoenix/markdownlint-rules/phoenix-rules.cjs"
    ],
    "markdownlint.run": "onSave",

    "prettier.requireConfig": False,
    "prettier.configPath": "./axion-core/standards/.prettierrc",

    "cSpell.configFile": "./axion-core/standards/cspell.jsonc",
    "cSpell.words": [
        "AISTF",
        "Badass",
        "chronos",
        "DQUEST",
        "dragonslayer",
        "EMPR",
        "Episemantics",
        "Freeplane",
        "Gamified",
        "Gemification",
        "GVRN",
        "HIER",
        "importmap",
        "Insforge",
        "INSFORGE",
        "KAELEN",
        "Lightbinder",
        "MAGN",
        "middleware",
        "Musashi",
        "Oathkeep",
        "Oathkeeper",
        "OGLN",
        "omni-anchor",
        "OSLM",
        "params",
        "PGPS",
        "PYREFLY",
        "Pythonic",
        "QLOR",
        "scanlines",
        "Serafina",
        "SUPABASE",
        "synarche",
        "SYNG",
        "trpc",
        "zustand"
    ],

    "search.exclude": {
        "**/__pycache__": True,
        "**/.mypy_cache": True,
        "**/.pytest_cache": True,
        "**/.ruff_cache": True,
        "**/node_modules": True,
        "**/dist": True,
        "**/out": True,
        "**/.tmp.*": True
    },
    "files.watcherExclude": {
        "**/__pycache__/**": True,
        "**/.mypy_cache/**": True,
        "**/.pytest_cache/**": True,
        "**/.ruff_cache/**": True,
        "**/.venv/**": True,
        "**/dist/**": True,
        "**/node_modules/**": True,
        "**/venv/**": True,
        "**/.git/**": True,
        "**/.vscode/**": True,
        "**/.trunk/**": True,
        "**/tmp.driveupload/**": True,
        "**/_logs/**": True,
        "**/artifacts/**": True,
        "**/scratch/**": True,
        "**/incoming/**": True,
        "**/_governance/**": True,
        "**/.archives/**": True,
        "**/.tmp.*": True
    },
    "errorLens.fontStyleItalic": True,
    "errorLens.fontWeight": "400",
    "errorLens.gutterIconsEnabled": True,
    "errorLens.messageBackgroundMode": "line",
    "sonarlint.rules": {
        "javascript:S106": "off"
    },
    "explorer.excludeGitIgnore": False,
    "files.autoSave": "off",
    "terminal.integrated.suggest.providers": {
        "lsp": True
    },
    "debug.console.closeOnEnd": True,
    "geminicodeassist.updateChannel": "Insiders",
    "python.analysis.autoFormatStrings": True,
    "python.analysis.autoImportCompletions": True,
    "terminal.integrated.drawBoldTextInBrightColors": False,
    "markdown.server.log": "debug",
    "python.analysis.referencesCodeLens": True,
    "python.analysis.inlayHints.variableTypes": True,
    "python.analysis.inlayHints.pytestParameters": True,
    "python.analysis.inlayHints.functionReturnTypes": True,
    "python.analysis.inlayHints.callArgumentNames": "partial",
    "powershell.codeFormatting.avoidSemicolonsAsLineTerminators": True,
    "python.analysis.enableTroubleshootMissingImports": True,
    "sonarlint.disableTelemetry": True,
    "trunk.addToolsToPath": True,
    "trunk.numJobs": 0,
    "trunk.workspaceFolderName": "📂 WORKSPACE ROOT",
    "notebook.defaultFormatter": "esbenp.prettier-vscode",

    "java.server.launchMode": "LightWeight",
    "java.jdt.ls.vmargs": "-Xmx128M -Xms64M -XX:+UseG1GC -XX:+UseStringDeduplication",
    "java.autobuild.enabled": False,
    "java.import.maven.enabled": False,
    "java.import.gradle.enabled": False,
    "java.import.gradle.wrapper.enabled": False,
    "java.project.importOnFirstTimeStartup": "disabled",
    "java.project.importOnFirstTimeStartup.showPrompts": False,
    "java.project.importHint": False,
    "java.recommendations.dependency.install": "false",
    "python.analysis.indexing.followSymlinkedFolders": False,
    "js/ts.preferences.importModuleSpecifier": "project-relative",
    "typescript.tsserver.maxTsServerMemory": 3072,
    "diffEditor.codeLens": True,
    "php.format.rules.addCommaAfterLastDeclParameter": True,
    "java.inlayHints.formatParameters.enabled": True,
    "java.inlayHints.parameterTypes.enabled": True,
    "markdown.extension.showActionButtons": True,
    "markdown.extension.completion.enabled": True,
    "markdown.preview.typographer": True,
    "powershell.buttons.showPanelMovementButtons": True,
    "powershell.codeFormatting.autoCorrectAliases": False,
    "powershell.codeFormatting.whitespaceBetweenParameters": True,
    "powershell.integratedConsole.showOnStartup": False,
    "prettier.experimentalTernaries": True,
    "[toml]": {
        "editor.defaultFormatter": "tamasfe.even-better-toml"
    },
    "python.analysis.completeFunctionParens": True,
    "python.pyrefly.configPath": "axion-core\\standards\\pyrefly.toml",
    "python.pyrefly.runnableCodeLens": True,
    "python.pyrefly.typeCheckingMode": "strict",

    "trunk.path": "C:\\Users\\Chris\\.cache\\trunk\\cli\\1.25.0-mingw-x86_64\\trunk.exe",
    "terminal.integrated.env.windows": {
        "PATH": "C:\\DevEnvironments\\master_env\\Scripts;${env:PATH}",
        "ESLINT_USE_FLAT_CONFIG": "true"
    },
    "code-runner.executorMap": {
        "python": "C:\\DevEnvironments\\master_env\\Scripts\\python.exe -u"
    },
    "code-runner.runInTerminal": True,
    "biome.configurationPath": "C://Users//Chris//Synarche_Workspace//axion-core//standards//biome.json",
    "vale.valeCLI.installVale": True,
    "vale.valeCLI.config": "${workspaceFolder}/.vale.ini",
    "vale.enableSpellcheck": True
}

# Write clean settings to file
with open("C:/Users/Chris/Synarche_Workspace/.vscode/settings.json", "w", encoding="utf-8") as f:
    json.dump(settings, f, indent=4)

print("SUCCESS: settings.json cleaned and validated.")
