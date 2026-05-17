# Findings

## 2026-05-15
- The central standards directory is firmly established at `C:\Users\Chris\Synarche_Workspace\axion-core\standards\`.
- We have scattered legacy configurations in `nova_forge` and `open-notebook` that need to be either merged or removed.
- Global user settings (VS Code and Antigravity) are currently pointing to a non-existent markdownlint config path (`.agent/substrate/rules/markdownlint/axion-rules.cjs`).
- The `.agent/substrate/rules/README.md` and `AGENT_AXION_SYNTHESIS.md` still reference old paths.
- `.agent/skills/core/lint-and-validate/scripts/lint_runner.py` relies on local config detection and does not fall back to the central `axion-core/standards/` configurations.
