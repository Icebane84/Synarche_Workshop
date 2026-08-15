#requires -Version 5.1
<#
.SYNOPSIS
    Phoenix Synarche - Linter & Formatter Environment Bootstrap (v2)

.DESCRIPTION
    Corrected against the actual, in-use .vscode/settings.json:

      - standards/ is NOT at the workspace root. It lives at
        <RepoRoot>/axion-core/standards/, and the workspace root is a
        multi-root layout with axion-core, phoenix-rosetta-stone,
        design-system, open-notebook, and nova_forge as siblings.
      - eslint-plugin-phoenix's custom markdownlint rules live one level
        deeper than assumed: eslint-plugin-phoenix/markdownlint-rules/, and
        there are TWO rule files there (axion-rules.cjs, phoenix-rules.cjs).
      - This script now MERGES into an existing .vscode/settings.json rather
        than overwriting it - a real settings.json carries ~100 unrelated
        personal editor keys (errorLens, Java, PHP, code-runner, etc.) that
        must survive a rerun.

    It still does NOT invent config content for standards/*. It validates
    presence, syncs the two files that must live outside standards/ to work
    (trunk.yaml, sonar-project.properties), and patches only the
    Phoenix-governed keys into .vscode/settings.json.

.PARAMETER RepoRoot
    Path to the multi-root workspace root (parent of axion-core/). Defaults
    to the current directory.

.PARAMETER StandardsRelativePath
    Path to the canonical config directory, relative to RepoRoot. Defaults to
    "axion-core/standards" per the real settings.json's own paths.

.PARAMETER PythonInterpreterPath / RuffExePath / MypyExePath / DmypyExePath / TrunkExePath
    Machine-specific tool paths. Optional - if omitted, the corresponding
    settings.json keys are left untouched (existing values, if any, are
    preserved rather than blanked out).

.PARAMETER Force
    Overwrite the two synced/generated files (.trunk/trunk.yaml,
    sonar-project.properties) even if they already exist.

.PARAMETER SkipTrunkCheck
    Skip the "trunk check --all" audit at the end (still installs/inits Trunk).
#>

[CmdletBinding()]
param(
    [string]$RepoRoot = (Get-Location).Path,
    [string]$StandardsRelativePath = 'axion-core/standards',
    [string]$PythonInterpreterPath,
    [string]$RuffExePath,
    [string]$MypyExePath,
    [string]$DmypyExePath,
    [string]$TrunkExePath,
    [switch]$Force,
    [switch]$SkipTrunkCheck
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

function Write-Step { param([string]$Message) Write-Host "`n[Phoenix Bootstrap] $Message" -ForegroundColor Cyan }
function Write-Ok { param([string]$Message) Write-Host "  [OK] $Message" -ForegroundColor Green }
function Write-Warn2 { param([string]$Message) Write-Host "  [WARN] $Message" -ForegroundColor Yellow }
function Write-Missing { param([string]$Message) Write-Host "  [MISSING] $Message" -ForegroundColor Red }

function Ensure-Directory {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Write-GeneratedFile {
    # For the small number of files that are legitimately regenerated
    # (copied) from the canonical standards/ source, because the tool that
    # consumes them requires a fixed location outside standards/.
    param(
        [Parameter(Mandatory = $true)][string]$SourcePath,
        [Parameter(Mandatory = $true)][string]$DestinationPath,
        [Parameter(Mandatory = $true)][string]$HeaderComment
    )
    if (-not (Test-Path -LiteralPath $SourcePath)) {
        Write-Missing "Cannot sync $DestinationPath - source not found: $SourcePath"
        return
    }
    if ((Test-Path -LiteralPath $DestinationPath) -and -not $Force) {
        Write-Warn2 "Keeping existing file (use -Force to resync): $DestinationPath"
        return
    }
    $parent = Split-Path -Parent $DestinationPath
    if ($parent) { Ensure-Directory -Path $parent }
    $body = Get-Content -LiteralPath $SourcePath -Raw
    $content = "$HeaderComment`n$body"
    [System.IO.File]::WriteAllText($DestinationPath, $content, [System.Text.UTF8Encoding]::new($false))
    Write-Ok "Synced: $DestinationPath  <-  $SourcePath"
}

function Test-CanonicalFile {
    param(
        [Parameter(Mandatory = $true)][string]$RelativePath,
        [Parameter(Mandatory = $true)][string]$GovernsTool,
        [switch]$Critical,
        [string]$BaseDir = $standardsDir
    )
    $full = Join-Path $BaseDir $RelativePath
    if (Test-Path -LiteralPath $full) {
        Write-Ok "$RelativePath  ->  $GovernsTool"
        return $true
    }
    else {
        Write-Missing "$RelativePath  ->  $GovernsTool  (expected at $full)"
        if ($Critical) { $script:hadCriticalMissing = $true }
        return $false
    }
}

function Ensure-Command {
    param([string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found. Install it first and rerun the script."
    }
}

function Ensure-Trunk {
    if (Get-Command trunk -ErrorAction SilentlyContinue) { return }
    Write-Step 'Installing Trunk CLI'
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id Trunk-io.Trunk -e --accept-source-agreements --accept-package-agreements
    }
    else {
        throw "Trunk CLI is required. Install it from https://docs.trunk.io/docs/install and rerun this script."
    }
    if (-not (Get-Command trunk -ErrorAction SilentlyContinue)) {
        throw 'Trunk CLI was not found after installation.'
    }
}

function Set-JsonSetting {
    # Adds/overwrites a single top-level key on a PSCustomObject, without
    # touching any of its other properties.
    param(
        [Parameter(Mandatory = $true)]$Target,
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)]$Value
    )
    $Target | Add-Member -NotePropertyName $Name -NotePropertyValue $Value -Force
}

# --------------------------------------------------------------------------
# Resolve paths
# --------------------------------------------------------------------------

$resolvedRepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
$standardsDir = Join-Path $resolvedRepoRoot ($StandardsRelativePath -replace '/', [System.IO.Path]::DirectorySeparatorChar)
$script:hadCriticalMissing = $false

# Workspace-relative forward-slash form, for embedding into settings.json
$standardsWsRel = "`${workspaceFolder}/$StandardsRelativePath"

Write-Step "Workspace root: $resolvedRepoRoot"
Write-Step "Standards (source of truth) directory: $standardsDir"

if (-not (Test-Path -LiteralPath $standardsDir)) {
    throw "Standards directory not found at '$standardsDir'. This script wires tooling to the existing " +
          "canonical configs; it does not invent them. Pass -StandardsRelativePath if your layout differs " +
          "from 'axion-core/standards'."
}

# --------------------------------------------------------------------------
# 1. Validate the canonical config set
# --------------------------------------------------------------------------

Write-Step 'Validating canonical config files (per axion-core/standards/README.md)'

Test-CanonicalFile -RelativePath 'pyproject.toml'          -GovernsTool 'Ruff / Black / pytest'         -Critical
Test-CanonicalFile -RelativePath 'pyrefly.toml'             -GovernsTool 'Pyrefly (Python type-check)'
Test-CanonicalFile -RelativePath 'mypy.ini'                  -GovernsTool 'mypy'                          -Critical
Test-CanonicalFile -RelativePath 'eslint.config.mjs'         -GovernsTool 'ESLint (flat config)'         -Critical
Test-CanonicalFile -RelativePath '.prettierrc'               -GovernsTool 'Prettier'                      -Critical
Test-CanonicalFile -RelativePath '.markdownlint.json'        -GovernsTool 'markdownlint'
Test-CanonicalFile -RelativePath '.markdownlint.cjs'         -GovernsTool 'markdownlint (extended rules)'
Test-CanonicalFile -RelativePath 'cspell.jsonc'              -GovernsTool 'CSpell'                        -Critical
Test-CanonicalFile -RelativePath 'sonar-project.properties'  -GovernsTool 'SonarQube'                     -Critical
Test-CanonicalFile -RelativePath 'dictionaries/master.jsonc' -GovernsTool 'CSpell (imported dictionary)'  -Critical
Test-CanonicalFile -RelativePath 'trunk.yaml'                -GovernsTool 'Trunk CLI'                     -Critical

Write-Step 'Validating the local ESLint "phoenix" plugin referenced by eslint.config.mjs'

Test-CanonicalFile -RelativePath 'eslint-plugin-phoenix/index.mjs'                         -GovernsTool 'phoenix/* rule registry' -Critical
Test-CanonicalFile -RelativePath 'eslint-plugin-phoenix/markdown-parser.cjs'               -GovernsTool 'markdown parser for eslint on *.md'
Test-CanonicalFile -RelativePath 'eslint-plugin-phoenix/rules/phoenix-logger.mjs'          -GovernsTool 'phoenix/use-phoenix-logger'
Test-CanonicalFile -RelativePath 'eslint-plugin-phoenix/rules/require-artifact-anchor.mjs' -GovernsTool 'phoenix/require-artifact-anchor'
Test-CanonicalFile -RelativePath 'eslint-plugin-phoenix/rules/enforce-sovereign-aliases.mjs' -GovernsTool 'phoenix/enforce-sovereign-aliases'
Test-CanonicalFile -RelativePath 'eslint-plugin-phoenix/rules/markdownlint.mjs'            -GovernsTool 'phoenix/markdownlint'

Write-Step 'Validating markdownlint custom rules (used by the VS Code markdownlint extension)'

Test-CanonicalFile -RelativePath 'eslint-plugin-phoenix/markdownlint-rules/axion-rules.cjs'  -GovernsTool 'Sentinel markdownlint rule engine' -Critical
Test-CanonicalFile -RelativePath 'eslint-plugin-phoenix/markdownlint-rules/phoenix-rules.cjs' -GovernsTool 'Phoenix markdownlint rule set'

if ($script:hadCriticalMissing) {
    Write-Warn2 'One or more CRITICAL config files are missing. Tooling wired below will fail until they exist.'
}

Write-Step 'Checking sibling project roots referenced by eslint.workingDirectories'
foreach ($sibling in @('phoenix-rosetta-stone', 'design-system', 'open-notebook', 'nova_forge')) {
    $siblingPath = Join-Path $resolvedRepoRoot $sibling
    if (Test-Path -LiteralPath $siblingPath) {
        Write-Ok "$sibling/"
    }
    else {
        Write-Warn2 "$sibling/ not found next to axion-core/ - ESLint's workingDirectories entry for it will no-op."
    }
}

# --------------------------------------------------------------------------
# 2. Known contradiction checks
# --------------------------------------------------------------------------

$pyprojectPath = Join-Path $standardsDir 'pyproject.toml'
$pyreflyPath = Join-Path $standardsDir 'pyrefly.toml'
if ((Test-Path -LiteralPath $pyprojectPath) -and (Test-Path -LiteralPath $pyreflyPath)) {
    if (Select-String -LiteralPath $pyprojectPath -Pattern '^\[tool\.pyrefly\]' -Quiet) {
        Write-Warn2 'CONTRADICTION: pyproject.toml defines [tool.pyrefly] AND pyrefly.toml exists standalone,'
        Write-Warn2 '  with different source-directories/search-path values. One is likely being silently'
        Write-Warn2 '  ignored (Pyrefly resolves precedence itself). Recommend deleting one of the two.'
    }
}

Write-Warn2 'FORMATTER CONFLICT: if your existing settings.json sets "biomejs.biome" as the default'
Write-Warn2 '  formatter for js/ts/json, note that neither README.md nor trunk.yaml list Biome as a'
Write-Warn2 '  governed tool - Prettier (.prettierrc) is the documented law for those extensions. This'
Write-Warn2 '  script will NOT silently switch your formatter; resolve this deliberately if it applies.'

# --------------------------------------------------------------------------
# 3. Sync the files that must live outside standards/ to function
# --------------------------------------------------------------------------

Write-Step 'Syncing files that tools require at a fixed location outside standards/'

Write-GeneratedFile `
    -SourcePath (Join-Path $standardsDir 'trunk.yaml') `
    -DestinationPath (Join-Path $resolvedRepoRoot '.trunk/trunk.yaml') `
    -HeaderComment "# GENERATED - synced from $StandardsRelativePath/trunk.yaml by bootstrap-phoenix-linter.ps1. Edit the source, not this file.`n"

Write-GeneratedFile `
    -SourcePath (Join-Path $standardsDir 'sonar-project.properties') `
    -DestinationPath (Join-Path $resolvedRepoRoot 'sonar-project.properties') `
    -HeaderComment "# GENERATED - synced from $StandardsRelativePath/sonar-project.properties by bootstrap-phoenix-linter.ps1. Edit the source, not this file.`n"

# --------------------------------------------------------------------------
# 4. Merge Phoenix-governed keys into .vscode/settings.json (preserving
#    every unrelated personal/editor setting already there)
# --------------------------------------------------------------------------

Write-Step 'Merging Phoenix-governed keys into .vscode/settings.json'

$vscodeDir = Join-Path $resolvedRepoRoot '.vscode'
Ensure-Directory -Path $vscodeDir
$settingsPath = Join-Path $vscodeDir 'settings.json'

if (Test-Path -LiteralPath $settingsPath) {
    $settings = Get-Content -LiteralPath $settingsPath -Raw | ConvertFrom-Json
    Write-Ok "Loaded existing settings.json ($((Get-Content -LiteralPath $settingsPath -Raw).Length) bytes) - unrelated keys will be preserved."
}
else {
    $settings = [PSCustomObject]@{}
    Write-Warn2 "No existing settings.json found - creating a new one with only Phoenix-governed keys."
}

# --- mypy ---
Set-JsonSetting $settings 'mypy-type-checker.args' @("--config-file", "$standardsWsRel/mypy.ini")
if ($MypyExePath) { Set-JsonSetting $settings 'mypy-type-checker.path' @($MypyExePath) }
if ($DmypyExePath) { Set-JsonSetting $settings 'mypy.dmypyExecutable' $DmypyExePath }

# --- Ruff ---
Set-JsonSetting $settings 'ruff.configuration' "$standardsWsRel/pyproject.toml"
Set-JsonSetting $settings 'ruff.configurationPreference' 'filesystemFirst'
Set-JsonSetting $settings 'ruff.importStrategy' 'fromEnvironment'
if ($RuffExePath) { Set-JsonSetting $settings 'ruff.path' @($RuffExePath) }
if ($PythonInterpreterPath) { Set-JsonSetting $settings 'ruff.interpreter' @($PythonInterpreterPath) }

# --- Python interpreter / interpreter-only if explicitly provided ---
if ($PythonInterpreterPath) {
    Set-JsonSetting $settings 'python.defaultInterpreterPath' $PythonInterpreterPath
}

# --- Pyrefly (correct camelCase key - the real settings.json had "configpath", a likely typo) ---
Set-JsonSetting $settings 'python.pyrefly.configPath' "$StandardsRelativePath/pyrefly.toml"
Set-JsonSetting $settings 'python.pyrefly.typeCheckingMode' 'strict'

# --- ESLint ---
Set-JsonSetting $settings 'eslint.useFlatConfig' $true
Set-JsonSetting $settings 'eslint.options' @{ overrideConfigFile = "$standardsWsRel/eslint.config.mjs" }
Set-JsonSetting $settings 'eslint.validate' @('javascript', 'typescript', 'typescriptreact', 'markdown')
Set-JsonSetting $settings 'eslint.run' 'onSave'

# --- Prettier (correct camelCase key - the real settings.json had "configpath", a likely typo) ---
Set-JsonSetting $settings 'prettier.configPath' "$standardsWsRel/.prettierrc"
Set-JsonSetting $settings 'prettier.requireConfig' $false

# --- CSpell ---
Set-JsonSetting $settings 'cSpell.configFile' "$standardsWsRel/cspell.jsonc"
Set-JsonSetting $settings 'cSpell.customWorkspaceDictionaries' @(
    @{
        name        = 'Phoenix Dictionary'
        path        = "$standardsWsRel/dictionaries/master.jsonc"
        addWords    = $true
        description = 'Master dictionary for the Phoenix Protocol'
    }
)

# --- markdownlint ---
Set-JsonSetting $settings 'markdownlint.customRules' @(
    "$standardsWsRel/eslint-plugin-phoenix/markdownlint-rules/axion-rules.cjs",
    "$standardsWsRel/eslint-plugin-phoenix/markdownlint-rules/phoenix-rules.cjs"
)
Set-JsonSetting $settings 'markdownlint.run' 'onSave'

# --- Formatter defaults per governed stack (Prettier for md/ts/json; Ruff for python) ---
# NOTE: deliberately NOT touching "[typescript]"/"[json]"/"editor.defaultFormatter" if a
# biomejs.biome association already exists there - see the FORMATTER CONFLICT warning above.
if (-not $settings.PSObject.Properties['[python]']) {
    Set-JsonSetting $settings '[python]' @{ 'editor.defaultFormatter' = 'charliermarsh.ruff' }
}
if (-not $settings.PSObject.Properties['[markdown]']) {
    Set-JsonSetting $settings '[markdown]' @{ 'editor.defaultFormatter' = 'esbenp.prettier-vscode' }
}

# --- Trunk ---
if ($TrunkExePath) { Set-JsonSetting $settings 'trunk.path' $TrunkExePath }
Set-JsonSetting $settings 'trunk.addToolsTopath' $true

$json = $settings | ConvertTo-Json -Depth 20
[System.IO.File]::WriteAllText($settingsPath, $json, [System.Text.UTF8Encoding]::new($false))
Write-Ok "Wrote merged: $settingsPath"

# --------------------------------------------------------------------------
# 5. Trunk CLI: install, init, sync ignores, run audit
# --------------------------------------------------------------------------

Write-Step 'Ensuring required tooling is available'
Ensure-Command -Name 'git'
Ensure-Trunk

Write-Step 'Initializing Trunk (using the synced .trunk/trunk.yaml)'
Push-Location $resolvedRepoRoot
try {
    trunk init --yes | Out-Null
    $trunkYamlPath = Join-Path $resolvedRepoRoot '.trunk/trunk.yaml'
    if (Test-Path -LiteralPath $trunkYamlPath) {
        $enabledLines = Select-String -LiteralPath $trunkYamlPath -Pattern '^\s*-\s+([a-zA-Z0-9_-]+)@' |
            ForEach-Object { $_.Matches[0].Groups[1].Value }
        if ($enabledLines) {
            Write-Step "Enabling linters declared in trunk.yaml: $($enabledLines -join ', ')"
            trunk check enable @enabledLines | Out-Null
        }
    }
}
finally {
    Pop-Location
}

if (-not $SkipTrunkCheck) {
    Write-Step 'Running the initial Phoenix audit'
    Push-Location $resolvedRepoRoot
    try {
        trunk check --all
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Warn2 'Skipped "trunk check --all" (-SkipTrunkCheck was set).'
}

# --------------------------------------------------------------------------
# Summary
# --------------------------------------------------------------------------

Write-Host "`nPhoenix bootstrap complete." -ForegroundColor Green
if ($script:hadCriticalMissing) {
    Write-Host 'One or more CRITICAL config files were missing - see [MISSING] lines above.' -ForegroundColor Red
}
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "  - Resolve the pyproject.toml / pyrefly.toml [tool.pyrefly] duplication (see WARN above)" -ForegroundColor Green
Write-Host "  - Decide on the Biome vs Prettier formatter conflict for js/ts/json, if it applies" -ForegroundColor Green
Write-Host "  - Populate any [MISSING] rule files under eslint-plugin-phoenix/rules/ and markdownlint-rules/" -ForegroundColor Green
Write-Host "  - Reload the VS Code window so .vscode/settings.json takes effect" -ForegroundColor Green
Write-Host "  - Run: trunk check --all" -ForegroundColor Green
