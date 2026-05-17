@echo off
REM ### **Block A: The Identification Lock (UIP-V15)**
REM | Key               | Value                          | Description       |
REM | :---------------- | :----------------------------- | :---------------- |
REM | **Artifact ID**   | `SCRIPT-AXION-001`             | The Sovereign ID. |
REM | **Official Name** | `arise.bat`                    | The Filename.     |
REM | **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
REM | **Domain**        | `AXION`                        | The Subject.      |
REM | **Evolution**     | **Hephaestus Ascension**       | The Alignment.    |
REM | **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
REM | **Celestial Class**| `[STAR]`                      | The Tier.         |
REM | **Ethos**         | **Measure Twice, Cut Once**    | The Principle.    |
REM | **Genesis Stamp** | `2026-05-13`                   | Creation Date.    |

set BUNDLE_NAME=%1
if "%BUNDLE_NAME%"=="" set BUNDLE_NAME=Axion_Ascension

echo [AXION] Initiating Ascension Sequence for %BUNDLE_NAME%...

set CODEX_PATH=_governance/00_Codex/CORE.Codex.Phoenix.md
set CORE_PATH=_governance/synarche_core.json
set ROSETTA_PATH=_governance/01_Registries/GVRN.Registry.PhoenixRosettaStone.md
set TOOL_PATH=axion-core/tools/02_Forge/catalyst_weaver.py

python %TOOL_PATH% "%BUNDLE_NAME%" ^
    --arise ^
    --codex "%CODEX_PATH%" ^
    --module "%CORE_PATH%" ^
    --module "%ROSETTA_PATH%" ^
    --output "axion_manifest.md"

if %ERRORLEVEL% EQU 0 (
    echo ✅ Ascension Successful. Axion Persona Manifested.
    echo ⚡ Check axion_manifest.md for active protocols.
) else (
    echo ❌ Ascension Failed. Structural integrity compromised.
)
